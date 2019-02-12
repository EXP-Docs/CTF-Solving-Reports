## [[Root-Me](https://www.root-me.org/)] [[Cracking](https://www.root-me.org/en/Challenges/Cracking/)] [[PE - 0 protection](https://www.root-me.org/en/Challenges/Cracking/PE-0-protection)] [[解题报告](http://exp-blog.com/2019/01/02/pid-2701/)]

------

不太水的水题，需要懂得反汇编工具的使用。

开始挑战后下载了一个 `ch15.exe` 文件，执行后无任何反应，判断只能反汇编，推荐使用 **OllyDBG** 工具。


使用 OllyDBG 打开 `ch15.exe` 文件后，右键 -> 中文搜索引擎 -> 搜索 ASCII ，可以找到成程序里面所有字符串常量。发现其中有一个 `Wrong password` 的文本提示，可以推断这个这个提示之前就是进行密码比对的代码，跳转到这个文本的位置。

不难发现， `Wrong password` 前面有多条 `jnz` 跳转语句，而每条 `jnz` 语句前都有一条 `cmp` 语句，由此可以推断代码逻辑是把输入字符串与真正的密码做逐字符比对，只要有一个字符不正确，则跳转到密码错误的提示。

那么很显然，只需要把每条 `cmp` 语句的十六进制常量依次串接，并还原成 ASCII ，就是真正的密码。

提取十六进制数列为 : `0x53 0x50 0x61 0x43 0x49 0x6f 0x53`。

使用 Burp Suite -> Decoder 工具对其解密还原成 ASCII ，得到密码，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B03%5D%20%5B5P%5D%20PE%20-%200%20protection/imgs/01.png)
![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B03%5D%20%5B5P%5D%20PE%20-%200%20protection/imgs/02.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2006~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
