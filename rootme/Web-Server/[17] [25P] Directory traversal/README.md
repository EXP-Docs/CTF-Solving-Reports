## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[Directory traversal](https://www.root-me.org/en/Challenges/Web-Server/Directory-traversal)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/web-server/directorytraversal/)]

------

这题要求找出画廊中隐藏的部分，而题目提示是目录遍历（Directory traversal）。

观察发现点击不同的分类， URL 中 `?galerie=${dir}` 会对应变化。

多次测试，当 `${dir}` 为空、即 `?galerie=` 时，会出现有一个展示所有子目录的漏洞。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B17%5D%20%5B25P%5D%20Directory%20traversal/imgs/01.png)

不难发现多了一个目录 `86hwnX2r` （注意渲染显示的目录名称不全，需要打开源码查看）。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B17%5D%20%5B25P%5D%20Directory%20traversal/imgs/02.png)

修改 URL 请求参数为 `?galerie=86hwnX2r` ，发现下面有一个文件 `password.txt`，查看源码知道该文件位置为 `galerie/86hwnX2r/password.txt`，拼接路径到根 URL （注意不要拼接到 URL 参数）即可查看到密码，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B17%5D%20%5B25P%5D%20Directory%20traversal/imgs/03.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
