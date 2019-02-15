## [[XSS-Game](https://xss-game.appspot.com/)] [[Level-5](https://xss-game.appspot.com/level5)] [[解题报告](http://exp-blog.com/2019/02/15/pid-3327/)]

------

关键找到注入点， Email 输入框只是障眼法，没有任何效果。

真正的注入点是 URL 的 `?next=` 参数，输入对应的内容，会改变 `Next >>` 超链的 href 属性值。

![](http://exp-blog.com/wp-content/uploads/2019/02/4f0be3afe89e620741659bfadbefba0b.png)

测试发现双引号和单引号均被过滤，即无法通过闭合引号注入属性。

但是 href 有最简单的注入方法，构造 payload ： `javascript:alert("exp")`

然后点击 Next 即可触发 alert ：

![](http://exp-blog.com/wp-content/uploads/2019/02/c9a01c229424d276d6ffcc4ffd4132be.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
