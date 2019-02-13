## [[Root-Me](https://www.root-me.org/)] [[Cracking](https://www.root-me.org/en/Challenges/Web-Client/)] [[Javascript - Obfuscation 3](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Obfuscation-3)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2916/)]

------

水题。一打开页面就弹出交互框要求输入密码，随便输入提示 `FAUX PASSWORD HAHA` 。

打开浏览器开发者工具，切到 Network 找到名为 `ch13.html` 中的一段 js 代码。

在代码里发现一个用来判断输入 `dechiffre` 函数，但是稍微分析下就知道这个函数的作用就是：无论输入什么都返回 `FAUX PASSWORD HAHA` （第一行的 `var pass = "70,65,85,88,32,80,65,83,83,87,79,82,68,32,72,65,72,65";` 就是这串提示的十进制ASCII码而已，用来混淆视听）。

关键是这个函数之后的一行代码：

`String["fromCharCode"](dechiffre("\x35\x35\x2c\x35\x36\x2c\x35\x34\x2c\x37\x39\x2c\x31\x31\x35\x2c\x36\x39\x2c\x31\x31\x34\x2c\x31\x31\x36\x2c\x31\x30\x37\x2c\x34\x39\x2c\x35\x30"));` 

这行代码与上下文无任何关系，但是它给出了一个提示：`fromCharCode` 表示 ASCII 解码，而后面是一串 `\x` 的十六进制数。

![](http://exp-blog.com/wp-content/uploads/2018/12/be7303a84a8e2109a5096e4d832d377d.png)

先手工把所有 `\x` 替换为空格，打开 Burp Suite -> Decoder ，进行 ASCII hex 解码。

解码后得到一串夹杂了很多空格和逗号的**伪十进制数字** ： 

`5 5 , 5 6 , 5 4 , 7 9 , 1 1 5 , 6 9 , 1 1 4 , 1 1 6 , 1 0 7 , 4 9 , 5 0`。

![](http://exp-blog.com/wp-content/uploads/2018/12/019105a1509cb01f280461d151238851.png)

手工将其整理下，得到真正的十进制 ASCII 编码： `55 56 54 79 115 69 114 116 107 49 50` 。
由于 Burp Suite **不支持**直接对**十进制 ASCII** 进行解码，先编码成十六进制，再进行 ASCII hex 解码，最后得到 `7 8 6 O s E r t k 1 2` 。

去掉空格串接起来就是真正的密码，完成挑战。

![](http://exp-blog.com/wp-content/uploads/2018/12/cae028df11093759e7c598429779f781.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
