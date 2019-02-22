## [[Root-Me](https://www.root-me.org/)] [[Web-Client](https://www.root-me.org/en/Challenges/Web-Client/)] [[Javascript - Source](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Source)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2902/)]

------

水题。一打开页面就弹出交互框要求输入密码，随便输入提示密码错误。

打开浏览器开发者工具，切到 Network 找到名为 `ch1.html` 中的一段 js 代码。

查看代码内容可以找到刚才的密码错误信息， `if` 的另一个分支就是密码正确的信息。

明显密码被写死在 `if` 的判断条件了，把密码拷过去，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B03%5D%20%5B5P%5D%20Javascript%20-%20Source/imgs/01.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
