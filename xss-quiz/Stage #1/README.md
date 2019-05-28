## [[xss-quiz](http://xss-quiz.int21h.jp/)] [[Stage #1](http://xss-quiz.int21h.jp)] [[解题报告](http://exp-blog.com/2019/05/29/pid-3847/)]

------

水题。题目要求是执行 JS 脚本 `alert(document.domain);`

不难发现在 Search 框输入的内容，不会做任何过滤直接输出到页面：

![](http://exp-blog.com/wp-content/uploads/2019/05/3ddd0c4203b3c6ce1bbaadf167704bce.png)

那么只需要构造以下 payload 到 Search 框，点击 Search 按钮即可完成挑战。

```javascript
<script>alert(document.domain);</script>
```

![](http://exp-blog.com/wp-content/uploads/2019/05/c5faf42adec3527c2266da3a21f22655.png)

> 本题用 Chrome 浏览器无法完成挑战（会被拦截），用 Firefox 则可完成挑战。

![](http://exp-blog.com/wp-content/uploads/2019/05/9ecafc78ff8e6e126b9eb3e3c110e92f.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
