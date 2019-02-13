## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[HTTP directory indexing](https://www.root-me.org/en/Challenges/Web-Server/HTTP-directory-indexing)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2966/)]

------

题目有个提示 `CTRL+U`，这个快捷键是查看源码的，在源码发现注释掉一行代码：`include("admin/pass.html")` 。

![](http://exp-blog.com/wp-content/uploads/2019/01/dd9823e984f142982f5dda5c0909be29.png)

在URL补全路径打开这个页面，用法语+英语双重嘲讽你被逗了。

![](http://exp-blog.com/wp-content/uploads/2019/01/5b02df762c64541ec03ded9467f4d368.png)

再想想题目是路径索引，或者是存在路径穿越一类的漏洞的，去掉URL中的 `pass.html` 看看有没有权限查看 `admin/` 目录。

结果猜中了，`admin` 目录下有个 `backup` 目录，然后有个 `admin.txt` 文件，密码就在里面，完成挑战。

![](http://exp-blog.com/wp-content/uploads/2019/01/47197d6a21e08b1d69b4a73305086f97.png)
![](http://exp-blog.com/wp-content/uploads/2019/01/b78afce8eca3ceb1c905b0b94f60052e.png)
![](http://exp-blog.com/wp-content/uploads/2019/01/fe44f10207591deed4c359dc93c33430.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
