## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[SQL injection - authentication](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-authentication)] [[解题报告](http://exp-blog.com/2019/03/10/pid-3538/)]

------


SQLi 水题，为了方便构造 payload 建议使用 Burp Suite 。

初步猜想 SQL 是这样的：

`select * from account where Login = '${Login}' and Password = '${Password}'`

Login 和 Password 都可以注入，注入任意一个即可。

由于题目要求我们找到 `administrator` 的密码，我们把 Login 的值固定为 `administrator` 就好了。

------------

在 Password 输入任意值提交，报错 `Error : no such user/password` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B31%5D%20%5B30P%5D%20SQL%20injection%20-%20authentication/imgs/01.png)

尝试在 Password 构造探针 ：`exp' or '1'='1` 。

虽然注入成功，但是查询结果只返回了一个账密： `user1 / TYsgv75zgtq` 。

> 不要着急用这个密码去验证，题目要求找到 administrator 的密码，而不是 user1 的密码。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B31%5D%20%5B30P%5D%20SQL%20injection%20-%20authentication/imgs/02.png)

换言之可能 `account` 表里面只有普通用户的账号记录，我们需要把目标转移到 **系统表**。

由此先想办法**找到数据库类型**，这样就可以间接确定系统表名称，再**跨表查询**。

------------

要知道数据库类型，可以尝试构造错误的 payload 令 SQL 解析失败，看看会不会抛出异常到前端。

尝试在 Password 构造 payload ：`'exp error'` （即不闭合引号），前端抛出异常，发现这是 SQLite3 数据库。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B31%5D%20%5B30P%5D%20SQL%20injection%20-%20authentication/imgs/03.png)

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

虽然这张表不是用来存储用户账密的，但还是尝试看看里面有什么。

在 Password 构造 payload 跨表查询 （注意末尾 `--` 注释掉原 SQL 中多余的内容） ：

`exp' or 1=1 union select name, sql from sqlite_master --`

获得 administrator 的密码，挑战成功。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B31%5D%20%5B30P%5D%20SQL%20injection%20-%20authentication/imgs/04.png)

> 其实这题不像是真正的数据库环境，感觉就是一个沙箱根据输入的内容做出对应的预设反应。

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
