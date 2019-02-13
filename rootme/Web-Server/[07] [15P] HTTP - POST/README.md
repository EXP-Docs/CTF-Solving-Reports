## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[HTTP - POST](https://www.root-me.org/en/Challenges/Web-Server/HTTP-POST)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2964/)]

------

水题，要求找到一种途径击败最高分。

打开浏览器开发者工具，切到 Elements，找到按钮的提交事件代码是 POST 一个分值，这个分值是在本地生成的一个随机数。

接下来就简单了，直接修改随机数生成代码为一个比 999999 大的固定值提交即可。

可以直接在浏览器修改，也可用 Burp Suite -> Repeater 修改提交表单的值，得到 flag 完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B07%5D%20%5B15P%5D%20HTTP%20-%20POST/imgs/01.png)
![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B07%5D%20%5B15P%5D%20HTTP%20-%20POST/imgs/02.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
