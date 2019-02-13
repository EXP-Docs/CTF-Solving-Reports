## [[Root-Me](https://www.root-me.org/)] [[Cracking](https://www.root-me.org/en/Challenges/Web-Client/)] [[Javascript - Obfuscation 1](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Obfuscation-1)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2909/)]

------

水题。一打开页面就弹出交互框要求输入密码，随便输入提示密码错误。

打开浏览器开发者工具，切到 Network 找到名为 `ch4.html` 中的一段 js 代码。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B05%5D%20%5B10P%5D%20Javascript%20-%20Obfuscation%201/imgs/01.png)

稍微分析下代码，发现密码被调用了`unescape`方法，即**密码被URL编码**了。

打开 Burp Suite -> Decoder ，直接**对密码进行URL解码**，得到真正的密码，完成挑战（注：使用其他在线的URL解码器也是一样的，一搜一大堆；甚至自己写代码进行解码也是OK的）。


![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B05%5D%20%5B10P%5D%20Javascript%20-%20Obfuscation%201/imgs/02.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
