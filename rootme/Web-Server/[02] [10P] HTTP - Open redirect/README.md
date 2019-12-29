## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[HTTP - Open redirect](https://www.root-me.org/en/Challenges/Web-Server/HTTP-Open-redirect)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2944/)]

------

打开挑战页面后，有3个点击后分别跳转到其他不同页面的按钮。

题目要求是：找到一种方式跳转到这3个页面之外的页面的方法。

打开浏览器开发者工具，切到 Elements ，可以看到这3个按钮分别触发一组URL参数： `?url=xxx&h=yyy` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B02%5D%20%5B10P%5D%20HTTP%20-%20Open%20redirect/imgs/01.png)

分析一下发现，页面会校验 `h` 的值后，再跳转到 `url`，而 `h` 的值是 `url` 的MD5 。

因此据此构造一个 get 参数的 payloads 即可：`?url=xxx&h=to_md5(xxx)` 。

MD5可以通过 Burp Suite -> Decoder 工具构造（也可以使用其他在线的MD5构造器）。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B02%5D%20%5B10P%5D%20HTTP%20-%20Open%20redirect/imgs/02.png)

发现在跳转过程中发现有个页面一闪而过，终止跳转或截图可以发现 flag 就在这个页面。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B02%5D%20%5B10P%5D%20HTTP%20-%20Open%20redirect/imgs/03.png)

此处推荐使用 Burp Suite -> Repeater 工具，直接拦截页面跳转，页面就不会一闪而过了。


![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B02%5D%20%5B10P%5D%20HTTP%20-%20Open%20redirect/imgs/04.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
