## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[HTTP - verb tampering](https://www.root-me.org/en/Challenges/Web-Server/HTTP-verb-tampering)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/web-server/http-verb-tampering/)]

------

题目已经提示：HTTP 动词篡改。 亦即通过不同的 HTTP 动词可能可以访问到不同的资源。

使用 Burp Suite -> Repeater 打开页面，修改 HTTP 请求的动词（原本为 `GET`），改成 `OPTIONS`、`PUT`、`DELETE` 中的任意一个均可获得密码，完成挑战。

> 注：根据 Burp Suite 分析可知当前页面遵循 HTTP/1.1 版本规范，这个版本支持 8 个动词：` GET`、`HEAD`、`POST`、`OPTIONS`、`PUT`、`DELETE`、`TRACE`、`CONNECT`，逐个试就行。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B10%5D%20%5B15P%5D%20HTTP%20verb%20tampering/imgs/01.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
