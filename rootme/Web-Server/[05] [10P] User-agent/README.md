## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[User-agent](https://www.root-me.org/en/Challenges/Web-Server/User-agent)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2956/)]

------

水题，打开挑战页面后提示：`Wrong user-agent: you are not the "admin" browser!` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B05%5D%20%5B10P%5D%20User-agent/imgs/01.png)

自然联想到修改 Request 参数的 User-Agent 值。

打开 Burp Suite -> Repeater 工具，直接修改 Headers 的 User-Agent 为 admin，提交请求。

从返回页面获得了密码，挑战完成。


![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B05%5D%20%5B10P%5D%20User-agent/imgs/02.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
