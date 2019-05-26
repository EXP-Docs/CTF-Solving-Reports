## [[RedTiger's Hackit](http://redtiger.labs.overthewire.org/)] [[Level 02 - Simple login-bypass](http://redtiger.labs.overthewire.org/level2.php)] [[解题报告](http://exp-blog.com/2019/05/26/pid-3812/)]

------

水题。

提示是使用 SQL 条件进行登陆绕过。

很容易发现在 Password 输入框构造 payload 为 `admin' or '1' = '1` 使得密码永真，则可成功绕过。

> 由于 Password 永真，Username 随便填即可

得到 flag 和通关密码，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/redtigers-hackit/Level%2002%20-%20Simple%20login-bypass/imgs/01.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
