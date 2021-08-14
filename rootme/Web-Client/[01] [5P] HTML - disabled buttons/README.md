## [[Root-Me](https://www.root-me.org/)] [[Web-Client](https://www.root-me.org/en/Challenges/Web-Client/)] [[HTML - disabled buttons](https://www.root-me.org/en/Challenges/Web-Client/HTML-disabled-buttons)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/web-client/html-disabled-buttons/)]

------

水题，其实标题就是提示，明显输入框和按钮都是处于不可用状态。

打开浏览器开发者工具，切到 Elements 查看 html 页面源码。

去掉输入框和按钮的 `disabled` 属性使其可用。

输入任意内容，点击按钮提交，可得到密码，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B01%5D%20%5B5P%5D%20HTML%20-%20disabled%20buttons/imgs/01.png)

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Client/%5B01%5D%20%5B5P%5D%20HTML%20-%20disabled%20buttons/imgs/02.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
