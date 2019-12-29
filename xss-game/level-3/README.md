## [[XSS-Game](https://xss-game.appspot.com/)] [[Level-3 ： That sinking feeling...](https://xss-game.appspot.com/level3)] [[解题报告](http://exp-blog.com/2019/02/15/pid-3331/)]

------

点击三个 `Image X` 按钮，发现页面会输出不同的图片，URL 末尾的数字也随之变化。

尝试在 URL 输入自定义的内容，发现页面会回显一个不存在的图片。

查看源码发现输入的内容被直接写入到 img 标签的 src 属性：

`<img src="/static/level3/cloud注入点.jpg">`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-3/imgs/01.png)

尝试构造 payload 闭合 img 的双引号：`" onerror=alert(1) "`

但是不起作用，明显双引号被过滤了：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-3/imgs/02.png)

测试发现单引号没有被过滤，于是可以用单引号闭合，成功构造 payload 如下：

`' onerror=alert("exp") '`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-3/imgs/03.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
