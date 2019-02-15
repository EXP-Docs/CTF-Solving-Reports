## [[XSS-Game](https://xss-game.appspot.com/)] [[Level-1](https://xss-game.appspot.com/level1)] [[解题报告](http://exp-blog.com/2019/02/15/pid-3299/)]

------

水题。

在 Search 框输入任意内容，如 `exp`，会跳转到输出页面 `?query=exp`，并把搜索内容回显到页面。

![](http://exp-blog.com/wp-content/uploads/2019/02/c95e752d91d60d894e291486c03a7547.png)

测试输入 `<img src=0 />`，发现页面未经过滤直接输出：

![](http://exp-blog.com/wp-content/uploads/2019/02/078ca27eee91c6411e007419abe7243f.png)

这就好办了，直接构造 payload 即可：

`<script>alert("exp")</script>`

![](http://exp-blog.com/wp-content/uploads/2019/02/730df9fe5a19ff45bcead1ea5a2e0dcc.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
