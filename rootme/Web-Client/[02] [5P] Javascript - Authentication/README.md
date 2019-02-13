## [[Root-Me](https://www.root-me.org/)] [[Cracking](https://www.root-me.org/en/Challenges/Web-Client/)] [[Javascript - Authentication](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Authentication)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2900/)]

------

水题。虽然页面没有任何提示，尝试随便输入一个账密，提示密码错误，一般都是隐藏起来了。

打开浏览器开发者工具，切到 Network 找到名为 `login.js` 的代码。

查看代码内容可以找到刚才的密码错误信息， `if` 的另一个分支就是密码正确的信息。

明显密码被写死在 `if` 的判断条件了，把密码拷过去，完成挑战。

![](http://exp-blog.com/wp-content/uploads/2018/12/8ea629cabf56ab698504d251915d5d1e.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
