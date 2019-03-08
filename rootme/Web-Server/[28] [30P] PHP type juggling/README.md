## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[PHP type juggling](https://www.root-me.org/en/Challenges/Web-Server/PHP-type-juggling)] [[解题报告](http://exp-blog.com/2019/03/07/pid-3508/)]

------


## 前置知识

> 这题无法在网页上解题，推荐用 **Burp Suite** 。

题目提示是 `PHP loose comparison`  ，即 PHP 得弱类型判定，相关知识点可以查看这几篇文章：

- [PHP strings comparison vulnerabilities](https://marcosvalle.github.io/ctf/php/2016/05/12/php-comparison-vlun.html) **【推荐】**
- [Strict vs. Loose Comparisons in PHP](https://www.copterlabs.com/strict-vs-loose-comparisons-in-php/)
- [PHP 函数漏洞总结](https://blog.csdn.net/qq_31481187/article/details/60968595?tdsourcetag=s_pcqq_aiomsg)
- [php strcmp()漏洞](https://blog.csdn.net/cherrie007/article/details/77473817?tdsourcetag=s_pcqq_aiomsg)

而其中与这挑战相关的漏洞主要有 3 个：

- `==` 的弱类型比较
- `strcmp()` 函数漏洞
- `0e` 开头的 MD5 （其实用不到，只是混淆项）

------------

## 题目分析

开启挑战后，页面只要求输入账号和密码：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B28%5D%20%5B30P%5D%20PHP%20type%20juggling/imgs/01.png)

点击 `Authentication source code` 后可查看页面源码：

```php
<?php

// $FLAG, $USER and $PASSWORD_SHA256 in secret file
require("secret.php");

// show my source code
if(isset($_GET['source'])){
    show_source(__FILE__);
    die();
}

$return['status'] = 'Authentication failed!';
if (isset($_POST["auth"]))  { 
    // retrieve JSON data
    $auth = @json_decode($_POST['auth'], true);

    // check login and password (sha256)
    if($auth['data']['login'] == $USER && !strcmp($auth['data']['password'], $PASSWORD_SHA256)){
        $return['status'] = "Access granted! The validation password is: $FLAG";
    }
}
print json_encode($return);

?>
```

很明显，只要能令 `$auth['data']['login'] == $USER` 和 `!strcmp($auth['data']['password'], $PASSWORD_SHA256)` 这两个条件为真，就可以令网页打印 `$FLAG` 。

而条件中的 `$USER` 和 `$PASSWORD_SHA256` 是定义在 `secret.php` 文件里面的常量，我们查看不到。唯一可以确认的是这两个常量的类型都是**字符串** ，而且 `$PASSWORD_SHA256` 是 **MD5** 。

而我们可以控制的输入点是 `$auth['data']['login']` 和 `$auth['data']['password']` 。

利用这两个输入点，我们可以逐一构造 payload 控制条件判定。

------------

## 利用 `==` 弱类型比较

首先是条件 `$auth['data']['login'] == $USER` 。

由于 `$USER` 是 **字符串** 类型，因此只需令 `$auth['data']['login']` 的值为 **数字 0** 即可使得这个条件判定为真。

这是因为 PHP 在比较 `数字 == 字符串` 时，会把字符串解析成数字 0 。

------------

## 利用 `strcmp()` 函数漏洞

接下来是条件 `!strcmp($auth['data']['password'], $PASSWORD_SHA256)` 。

注意到题目特意在前面加了一个 `!` 取反，换言之我们的目的是令 `strcmp` 的返回值为 `0` 。

在正常情况下，当且仅当 `strcmp` 所比较的两个字符串相同时，才会返回 0 。

但是我们不知道 `$PASSWORD_SHA256` 的值，所以只能**从非正常情况下**考虑。

所谓的非正常情况，是指当 `strcmp` 的**两个参数不全是字符串**的情况：

- 当 PHP 版本低于 5.2 时，会将两个参数先转换成字符串类型再比较
- 当 PHP 版本高于 5.3.3 时，**若一个参数是数组，另一个参数是字符串时，除了抛出异常，还会返回 0**
- 当 PHP 版本高于 5.5 后，如果任意一个参数不是字符串类型，直接返回 null

从出题角度去考虑，只有第二个情况可以被我们利用，因此猜测题目的 PHP 版本应该是 5.3.3 。

于是，不妨令 `$auth['data']['password']` 的值为数组 `[]` 。

------------

## 构造 payload

结合前面分析，最终我们尝试构造这样的 payload ：

在`Your login` 输入 `0` ，在 `Your password` 输入 `[]` 。但是不起任何作用。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B28%5D%20%5B30P%5D%20PHP%20type%20juggling/imgs/02.png)

使用 Burp Suite 捕获刚才的请求，发现我们输入的参数被转换成 Json ：

```json
{"data":{"login":"0","password":"4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"}}
```

明显两个输入的参数都被转换成了字符串，甚至 `[]` 还被加密成 MD5 ，这样自然无法使我们的 payload 生效。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B28%5D%20%5B30P%5D%20PHP%20type%20juggling/imgs/03.png)


于是直接在 Burp Suite 修改 Json 的参数，即构造真正的 payload 如下 （注意**类型**分别是**数字**和**数组**）：

```json
{"data":{"login":0,"password":[]}}
```

成功控制条件，得到 flag ，完成挑战：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B28%5D%20%5B30P%5D%20PHP%20type%20juggling/imgs/04.png)

------------

## 附：关于 `0e` 开头的 MD5 漏洞

`0e` 其实是科学计数法的开头，例如 `0e2` 表示 `0 x 10^2` 。

而当使用 `==` 比较 MD5 字符串，若恰好 MD5 是以 `0e` 开头，就会被判定为数字类型，可以用来绕过某些情况。

虽然这题的 password 用 MD5 加密，但其实是混淆项，因为比较 MD5 使用的是 `strcmp()` 函数而非 `==` 操作符。

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
