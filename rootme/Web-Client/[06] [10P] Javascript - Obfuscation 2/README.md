## [[Root-Me](https://www.root-me.org/)] [[Web-Client](https://www.root-me.org/en/Challenges/Web-Client/)] [[Javascript - Obfuscation 2](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Obfuscation-2)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2911/)]

------

水题，熟悉编码的样子就很容易做。

打开页面什么都没有，打开浏览器开发者工具，切到 Network 找到名为 `ch12.html` 中的一段 js 代码。

发现密码被定义为：

`var pass = unescape("unescape%28%22String.fromCharCode%2528104%252C68%252C117%252C102%252C106%252C100%252C107%252C105%252C49%252C53%252C54%2529%22%29");`

其中两次 `unescape` 表示要做**两次 URL 解码**，`fromCharCode`表示要做**一次 ASCII 解码**。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B06%5D%20%5B10P%5D%20Javascript%20-%20Obfuscation%202/imgs/01.png)

打开 Burp Suite -> Decoder ，做**两次 URL 解码**得到 ：

`unescape("String.fromCharCode(104,68,117,102,106,100,107,105,49,53,54)")`

由于 Burp Suite **不支持**直接对**十进制 ASCII** 进行解码，所以先将其**编码成十六进制**，得到：

`68,44,75,66,6a,64,6b,69,31,35,36` 

最后对这串**十六进制 ASCII 解码**，得到真正的11个字符： `h,D,u,f,j,d,k,i,1,5,6` 。

去掉逗号串起来就是真正的密码，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B06%5D%20%5B10P%5D%20Javascript%20-%20Obfuscation%202/imgs/02.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
