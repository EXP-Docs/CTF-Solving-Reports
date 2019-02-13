## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[Directory traversal](https://www.root-me.org/en/Challenges/Web-Server/Directory-traversal)] [[解题报告](http://exp-blog.com/2019/01/14/pid-2993/)]

------

这题要求找出画廊中隐藏的部分，而题目提示是目录遍历（Directory traversal）。

观察发现点击不同的分类， URL 中 `?galerie=${dir}` 会对应变化。

多次测试，当 `${dir}` 为空、即 `?galerie=` 时，会出现有一个展示所有子目录的漏洞。

![](http://exp-blog.com/wp-content/uploads/2019/01/0edb2255c55641c54d108383969ac766.png)

不难发现多了一个目录 `86hwnX2r` （注意渲染显示的目录名称不全，需要打开源码查看）。

![](http://exp-blog.com/wp-content/uploads/2019/01/7d337fa1cbefda88fcfb4504dfbb9790.png)

修改 URL 请求参数为 `?galerie=86hwnX2r` ，发现下面有一个文件 `password.txt`，查看源码知道该文件位置为 `galerie/86hwnX2r/password.txt`，拼接路径到根 URL （注意不要拼接到 URL 参数）即可查看到密码，完成挑战。

![](http://exp-blog.com/wp-content/uploads/2019/01/92370b4407ec1bc7cecb12e1aae2f14b.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
