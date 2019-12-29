## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[HTTP directory indexing](https://www.root-me.org/en/Challenges/Web-Server/HTTP-directory-indexing)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2966/)]

------

题目有个提示 `CTRL+U`，这个快捷键是查看源码的，在源码发现注释掉一行代码：`include("admin/pass.html")` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B08%5D%20%5B15P%5D%20HTTP%20directory%20indexing/imgs/01.png)

在URL补全路径打开这个页面，用法语+英语双重嘲讽你被逗了。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B08%5D%20%5B15P%5D%20HTTP%20directory%20indexing/imgs/02.png)

再想想题目是路径索引，或者是存在路径穿越一类的漏洞的，去掉URL中的 `pass.html` 看看有没有权限查看 `admin/` 目录。

结果猜中了，`admin` 目录下有个 `backup` 目录，然后有个 `admin.txt` 文件，密码就在里面，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B08%5D%20%5B15P%5D%20HTTP%20directory%20indexing/imgs/03.png)
![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B08%5D%20%5B15P%5D%20HTTP%20directory%20indexing/imgs/04.png)
![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B08%5D%20%5B15P%5D%20HTTP%20directory%20indexing/imgs/05.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
