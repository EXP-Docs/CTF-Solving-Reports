# CTF-Solving-Reports
　[[Root-Me](https://www.root-me.org/)] [[Cracking](https://www.root-me.org/en/Challenges/Cracking/)] [[ELF - 0 protection](https://www.root-me.org/en/Challenges/Cracking/ELF-0-protection)] [[解题报告](http://exp-blog.com/2019/01/02/pid-2703/)]

------

水题，需要知道的是 `ELF` 是 Linux 下的一种可执行的二进制文件（类比 Windows 的 `exe`）。

开始挑战后下载了一个 `ch1.zip` 文件，解压后得到 `ch1.bin`。

使用 **UE编辑器** 打开查看文件内容，基本都是乱码，但是切换到十六进制模式还是可以找到一些关键性代码的。

发现其中有一段用法语写的提示 `Veuillez entrer le mot de passe :  pass : %s!` `.....Dommage, essaye encore une fois.` ，大意是：请输入密码，密码错误请重新输入。

怀疑这部分就是判断密码的逻辑，那么前面很可能有真正的密码比对，以触发这段代码。

向上找果然找到有一段代码 `Allocating memory.Reallocating memory.123456789..`，大意是把 `123456789` 重新载入内存。

其实这就是密码，这么直白地把密码明文存储也是没谁了，完成挑战。

![](http://exp-blog.com/wp-content/uploads/2019/01/29e8355b99ba81e8aed9e018655a8ae6.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2006~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
