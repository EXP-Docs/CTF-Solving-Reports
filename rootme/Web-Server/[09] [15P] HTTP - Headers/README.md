## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[HTTP - Headers](https://www.root-me.org/en/Challenges/Web-Server/HTTP-Headers)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/web-server/http-headers/)]

------

题目要求使用 administrator 权限查看页面，页面提示：一个HTTP响应不仅仅只有 Content 。

这个提示已经很直白了，除了 Content 还有的就是 Header，然后查一下 Respone Header 发现有个参数 `Header-RootMe-Admin: none` ， 很可能目标就是为这个参数设置值。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B09%5D%20%5B15P%5D%20HTTP%20Headers/imgs/01.png)

使用 Burp Suite -> Repeater 打开页面，修改 Request 的 Header ，添加属性 `Header-RootMe-Admin` ，**值为任意值**，然后发起请求，得到密码，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B09%5D%20%5B15P%5D%20HTTP%20Headers/imgs/02.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
