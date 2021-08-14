## [[xss-quiz](http://xss-quiz.int21h.jp/)] [[Stage #1](http://xss-quiz.int21h.jp)] [[解题报告](https://exp-blog.com/safe/ctf/xss-quiz/stage-1/)]

------

水题。题目要求是执行 JS 脚本 `alert(document.domain);`

不难发现在 Search 框输入的内容，不会做任何过滤直接输出到页面：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-quiz/Stage%20%231/imgs/01.png)

那么只需要构造以下 payload 到 Search 框，点击 Search 按钮即可完成挑战。

```javascript
<script>alert(document.domain);</script>
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-quiz/Stage%20%231/imgs/02.png)

> 本题用 Chrome 浏览器无法完成挑战（会被拦截），用 Firefox 则可完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/xss-quiz/Stage%20%231/imgs/03.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
