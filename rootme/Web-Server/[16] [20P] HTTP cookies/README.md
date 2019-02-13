## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[HTTP cookies](https://www.root-me.org/en/Challenges/Web-Server/HTTP-cookies)] [[解题报告](http://exp-blog.com/2019/01/14/pid-2991/)]

------

输入任意 email 后，点击 `Saved email adresses` 后提示 `You need to be admin` 。

![](http://exp-blog.com/wp-content/uploads/2019/01/7250ce9e9f47888933402de4382dde2f.png)

在页面源码发现注释了一行代码 `<!--SetCookie("ch7","visiteur");-->`，检查 Cookie 发现当前 `ch7=visiteur` 。

使用 Burp Suite -> Repeater 模拟 `Saved email adresses` 提交行为，修改 Cookie 为 `ch7=admin` ，提交后得到密码，完成挑战。


![](http://exp-blog.com/wp-content/uploads/2019/01/720e7c65e4bee1128d50f4a69ab60659.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
