## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[CRLF](https://www.root-me.org/en/Challenges/Web-Server/CRLF)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2981/)]

------

题目有2个提示：

- CRLF
- 注入异常数据到日志（Inject false data in the journalisation log）

打开挑战页面后，发现三行初始日志，稍微分析下：

```
# Authentication log
admin failed to authenticate.    # admin 认证失败
admin authenticated.                # admin 认证成功
guest failed to authenticate.     # guest 认证成功
```

在登录框随便输入一些内容，日志会刷新一行： `${username} failed to authenticate.`，而 password 的内容不会打印到日志，亦即我们可以控制的输入位置为 `${username}` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B13%5D%20%5B20P%5D%20CRLF/imgs/01.png)

到此可以基本推断出：我们需要在 username 的输入框中进行注入某个 payloads，使得日志中打印一行 `guest  authenticated.` 进行欺骗。

注入方式是题目已提示是 `CRLF`，即回车换行，对应的 URL 编码是 `%0d%0a`  （注意空格的 URL 编码是 `%20`）。

使用 Burp Suite -> Repeater 打开页面，在 HTTP 请求参数设置 payloads ：

`?username=guest%20authenticated.%0d%0aexp&password=none`

提交后成功欺骗，获得密码，完成挑战。


![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B13%5D%20%5B20P%5D%20CRLF/imgs/02.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
