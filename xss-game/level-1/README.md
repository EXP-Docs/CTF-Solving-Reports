## [[XSS-Game](https://xss-game.appspot.com/)] [[Level-1 : Hello, world of XSS](https://xss-game.appspot.com/level1)] [[解题报告](http://exp-blog.com/2019/02/15/pid-3299/)]

------

水题。

在 Search 框输入任意内容，如 `exp`，会跳转到输出页面 `?query=exp`，并把搜索内容回显到页面。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-1/imgs/01.png)

测试输入 `<img src=0 />`，发现页面未经过滤直接输出：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-1/imgs/02.png)

这就好办了，直接构造 payload 即可：

`<script>alert("exp")</script>`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-1/imgs/03.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
