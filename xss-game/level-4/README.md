## [[XSS-Game](https://xss-game.appspot.com/)] [[Level-4](https://xss-game.appspot.com/level4)] [[解题报告](http://exp-blog.com/2019/02/15/pid-3329/)]

------

输入任意数值 n ，页面会阻塞计时 n 秒。

输入一个较大的数值让页面停留在计时页面，然后查看页面源码可以看到 JS 代码。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-4/imgs/01.png)

从 JS 代码可以找到注入点在这里：

`<img src="/static/loading.gif" onload="startTimer('注入点');">`

闭合单引号和括号，构造 payload ： `1');alert('exp`

即相当于变成这样： `startTimer('1');alert('exp');` ，成功突破。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-4/imgs/02.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
