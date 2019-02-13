## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[HTTP verb tampering](https://www.root-me.org/en/Challenges/Web-Server/HTTP-verb-tampering)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2972/)]

------

题目已经提示：HTTP 动词篡改。 亦即通过不同的 HTTP 动词可能可以访问到不同的资源。

使用 Burp Suite -> Repeater 打开页面，修改 HTTP 请求的动词（原本为 `GET`），改成 `OPTIONS`、`PUT`、`DELETE` 中的任意一个均可获得密码，完成挑战。

> 注：根据 Burp Suite 分析可知当前页面遵循 HTTP/1.1 版本规范，这个版本支持 8 个动词：` GET`、`HEAD`、`POST`、`OPTIONS`、`PUT`、`DELETE`、`TRACE`、`CONNECT`，逐个试就行。

![](http://exp-blog.com/wp-content/uploads/2019/01/e97ee1f76b30bacd8451617a88b40cb9.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
