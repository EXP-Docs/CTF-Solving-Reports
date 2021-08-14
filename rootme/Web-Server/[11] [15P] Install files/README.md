## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[Install files](https://www.root-me.org/en/Challenges/Web-Server/Install-files)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/web-server/install-files/)]

------

不是猫扑、天涯那个年代的程序员对这题可能很陌生了。

打开页面什么都没有，查看页面源码发现有一行注释：`<!--  /web-serveur/ch6/phpbb -->` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B11%5D%20%5B15P%5D%20Install%20files/imgs/01.png)

在页面 URL 后面补充 `phpbb` ，再打开页面依然什么也没有。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B11%5D%20%5B15P%5D%20Install%20files/imgs/02.png)

搜索一下 phpbb，知道这是一个曾经很火 BBS 开源论坛软件。

再结合题眼考虑：Install files （安装文件）。。。有可能是要找到 phpbb 的安装文件的信息。

测试了几个可能的安装目录名称，最终发现在 URL 后面补充  `phpbb/install/` 可以查看安装目录，里面有个 `install.php` 文件，打开后找到密码，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B11%5D%20%5B15P%5D%20Install%20files/imgs/03.png)
![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B11%5D%20%5B15P%5D%20Install%20files/imgs/04.png)

> install.php 里面用法文描述了这个挑战的故事背景，翻译一下就是：
<br/>　　　恭喜，您刚刚发现了phpBB中的众多缺陷之一。
<br/>　　　事实上，这个缺陷是网站管理员的疏忽，配置了敏感信息的安装文件没有被删除。
<br/>　　　你必须要了解的是我们经常会通过 **篡改URL** 发现很多东西 ...
<br/>　　　也多亏了他们的疏忽，现在你可以重置论坛，并更改所有密码，然后完全控制论坛!!
<br/>　　　要验证的密码是：`karambar`
<br/>　　　祝你好运！

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
