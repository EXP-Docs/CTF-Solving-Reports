## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[PHP register globals](https://www.root-me.org/en/Challenges/Web-Server/PHP-register-globals)] [[解题报告](http://exp-blog.com/2019/03/05/pid-3456/)]

------

前置知识可以参考 [这里](http://php.net/manual/zh/security.globals.php) 。

大概意思就是，register_globals 是 PHP 的一个特性，在 4.2.0 版本之前，它是默认启用的。

当它启用的时候，PHP 会允许变量未初始化就使用（换言之在第一次使用的时候就是初始化的时候），这样就使得变量的来源变得不确定。

于是就可能直接在 URL 以传参的方式（如 `?key=val`）胁持变量初始化，若 PHP 代码没有考虑这种情况，就存在被入侵的风险。


------------

知道这个知识点后，回到这题。

开启挑战后进入一个页面，但是找不到任何注入点。虽然说提示是 register_globals ，但是不知道应该挟持哪个变量也是于事无补。

因此应该先想办法找到页面的 PHP 代码，从而找到可能被挟持的变量。


------------

注意到题目的另一个提示是（**开发者经常留下备份文件**）：

`It seems that the developper often leaves backup files around...`

虽然不难测试到主页名称是 `index.php` ，但是要找到它的备份名称也不是容易的事情，只能靠猜。

最终猜到备份页面名称为 `index.php.bak` （其实我真的很不喜欢猜文件名。。变成全凭运气解题好无语）

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B21%5D%20%5B25P%5D%20PHP%20register%20globals/imgs/01.png)

下载 [`index.php.bak`](http://challenge01.root-me.org/web-serveur/ch17/index.php.bak)  后得到页面的 PHP 代码为：

```php
<?php


function auth($password, $hidden_password){
    $res=0;
    if (isset($password) && $password!=""){
        if ( $password == $hidden_password ){
            $res=1;
        }
    }
    $_SESSION["logged"]=$res;
    return $res;
}



function display($res){
    $aff= '
    <html>
    <head>
    </head>
    <body>
      <h1>Authentication v 0.05</h1>
      <form action="" method="POST">
        Password <br/>
        <input type="password" name="password" /><br/><br/>
        <br/><br/>
        <input type="submit" value="connect" /><br/><br/>
      </form>
      <h3>'.htmlentities($res).'</h3>
    </body>
    </html>';
    return $aff;
}



session_start();
if ( ! isset($_SESSION["logged"]) )
    $_SESSION["logged"]=0;

$aff="";
include("config.inc.php");

if (isset($_POST["password"]))
    $password = $_POST["password"];

if (!ini_get('register_globals')) {
    $superglobals = array($_SERVER, $_ENV,$_FILES, $_COOKIE, $_POST, $_GET);
    if (isset($_SESSION)) {
        array_unshift($superglobals, $_SESSION);
    }
    foreach ($superglobals as $superglobal) {
        extract($superglobal, 0 );
    }
}

if (( isset ($password) && $password!="" && auth($password,$hidden_password)==1) || (is_array($_SESSION) && $_SESSION["logged"]==1 ) ){
    $aff=display("well done, you can validate with the password : $hidden_password");
} else {
    $aff=display("try again");
}

echo $aff;

?>

```

从代码不难分析到关键点是这段代码，当条件为真时，它会打印真正的密码 `$hidden_password` :

```php
if (( isset ($password) && $password!="" && auth($password,$hidden_password)==1) || 
        (is_array($_SESSION) && $_SESSION["logged"]==1 ) ){
    $aff=display("well done, you can validate with the password : $hidden_password");
} else {
    $aff=display("try again");
}
```


而要令条件为真，可以利用 `||` 后面的的条件 `(is_array($_SESSION) && $_SESSION["logged"]==1 )` ，

即我们要通过 register_globals 挟持的变量是 `_SESSION["logged"]` ，并将其初始化为 1 。

为此可以构造这样的 payload （测试发现双引号会被过滤，因此直接去掉亦可）：

`http://challenge01.root-me.org/web-serveur/ch17/?_SESSION[logged]=1`

挟持变量成功，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B21%5D%20%5B25P%5D%20PHP%20register%20globals/imgs/02.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
