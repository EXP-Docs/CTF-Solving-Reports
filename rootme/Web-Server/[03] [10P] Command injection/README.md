## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[Command injection](https://www.root-me.org/en/Challenges/Web-Server/Command-injection)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2946/)]

------

这题有两个提示：

- 命令注入
- flag 在 index.php 文件里面

打开页面后，输入 127.0.0.1 提交，可以看见回显。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B03%5D%20%5B10P%5D%20Command%20injection/imgs/01.png)

从回显结果来看，代码实现应该是调用了 系统命令，因此这里可以考虑使用管道 `|` 注入命令。

输入 `| ls -al` 提交，回显打印了当前目录的文件列表，从中发现了 `index.php` 文件。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B03%5D%20%5B10P%5D%20Command%20injection/imgs/02.png)

构造 payloads 为  `| cat index.php` 提交，发现页面嵌套渲染了另一个 `index.php` 页面。

打开浏览器开发者工具，切到 Elements，看到嵌套页面的 PHP源码，其中有个 `$flag` 变量，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B03%5D%20%5B10P%5D%20Command%20injection/imgs/03.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
