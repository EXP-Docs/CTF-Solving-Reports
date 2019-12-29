## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[Improper redirect](https://www.root-me.org/en/Challenges/Web-Server/Improper-redirect)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2977/)]

------

题目有 3 个提示：

- 错误的重定向（Improper redirect）
- 不要相信你的浏览器（Don’t trust your browser）
- 尝试访问首页（Get access to index）

打开挑战页面，发现是登录页面， URL 后缀是 `?redirect` ，即这是通过重定向跳转过来的页面，但究竟是从哪里重定向过来的呢？

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B12%5D%20%5B15P%5D%20Improper%20redirect/imgs/01.png)

结合提示猜测应是从首页跳转过来的，删除 URL 的 `login.php?redirect` 再访问，会触发跳转，但依然看不到信息。

使用 Burp Suite -> Repeater 打开首页，避免自动跳转页面，可以看到 302 页面的信息，flag 就在里面，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B12%5D%20%5B15P%5D%20Improper%20redirect/imgs/02.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
