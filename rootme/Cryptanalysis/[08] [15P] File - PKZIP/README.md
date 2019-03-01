## [[Root-Me](https://www.root-me.org/)] [[Cryptanalysis](https://www.root-me.org/en/Challenges/Cryptanalysis/)] [[File - PKZIP](https://www.root-me.org/en/Challenges/Cryptanalysis/File-PKZIP)] [[解题报告](http://exp-blog.com/2019/03/02/pid-3441/)]

------

送分题。

开启挑战后下载了一个加密的压缩包，让我们破解压缩包的密码。

题目提示是 PKZIP 压缩格式，而且给了一份 [PDF](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cryptanalysis/%5B08%5D%20%5B15P%5D%20File%20-%20PKZIP/EN%20-%20Cracking%20PKZIP%20file's%20password.pdf) 指引。

通篇意思就是让我们去了解一下 PKZIP 的文件格式，然后找到一份足够大的密码字典表，暴力破解。。。

还很贴心在末尾提供了一份 C++ 代码。


题目是 2010 年出的了，现在已经过了 9 年了，，，现成的暴力破解工具多的是。。。

例如我找到的这个工具 【[PackageCrack.exe](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cryptanalysis/%5B08%5D%20%5B15P%5D%20File%20-%20PKZIP/PackageCrack.zip)】，直接就破解成功了：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cryptanalysis/%5B08%5D%20%5B15P%5D%20File%20-%20PKZIP/imgs/01.png)


> Linux 下可使用工具 【[fcrackzip](https://github.com/hyc/fcrackzip)】 破解



------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
