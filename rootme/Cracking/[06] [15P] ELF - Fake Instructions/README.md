## [[Root-Me](https://www.root-me.org/)] [[Cracking](https://www.root-me.org/en/Challenges/Cracking/)] [[ELF - Fake Instructions](https://www.root-me.org/en/Challenges/Cracking/ELF-Fake-Instructions)] [[解题报告](http://exp-blog.com/2019/02/27/pid-3413/)]

------

## 前言

【[Cracking : ELF C++ - 0 protection](https://github.com/lyy289065406/CTF-Solving-Reports/tree/master/rootme/Cracking/%5B05%5D%20%5B10P%5D%20PE%20DotNet%20-%200%20protection)】 的进阶篇。

开启挑战后下载了 `ch4.zip` ，解压后得到文件 `crackme` 。

题目已经提示了这是用 gcc 编译的 ELF 32-bit 文件，即使没提示，也可在 Linux 通过命令 `file crackme` 查看：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B06%5D%20%5B15P%5D%20ELF%20-%20Fake%20Instructions/imgs/01.png)

------------

## 试错

把文件 `crackme` 上传到 Linux ，执行命令 `chomd u+x crackme` 赋予脚本执行权限。

然后执行命令 `./crackme` ，提示使用方式为： `(*) -Syntaxe: ./crackme [password] `

根据提示再次执行命令 `./crackme www.exp-blog.com` （其中 `www.exp-blog.com` 是随意输入的密码）

此时会用法语提示密码错误：

```
Vérification de votre mot de passe..
le voie de la sagesse te guidera, tache de trouver le mot de passe petit padawaan
```

------------

## 源码分析

有了这些提示，我们可以开始从源码缩小并定位密码判定语句的位置。

在 Windows 使用 IDA 工具反汇编此文件，通过 Search -> text...  查找密码错误的提示关键字 `padawaan` ，

在数据段找到变量名 `aLeVoieDeLaSage` ，右击，选择 `Jump to xref to operand...` 跳转到引用位置。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B06%5D%20%5B15P%5D%20ELF%20-%20Fake%20Instructions/imgs/02.png)


当前跳转到 `RSA` 函数，未发现的比较关键代码。

再次右击 `RSA` 函数，选择 `Jump to xref to operand...` 跳转到引用位置。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B06%5D%20%5B15P%5D%20ELF%20-%20Fake%20Instructions/imgs/03.png)

这次跳转到 `WPA` 模块的关键位置，在执行字符串比较语句 `call _strcmp` 之后：

- `test eax, eax` ： 利用 `eax` 寄存器的值对 `ZF` 标志位置位
- `jnz` ： 当 `ZF == 0 ` 时走 `blowfish` 红色分支，当 `ZF != 0 ` 时走 `RSA` 绿色分支

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B06%5D%20%5B15P%5D%20ELF%20-%20Fake%20Instructions/imgs/04.png)

而 `RSA` 绿色分支是我们前面利用密码错误的提示逆向找到的分支。

换言之 `blowfish` 红色分支才是密码正确时会走的分支，即我们的目标分支。

但是查看 `blowfish` 分支的源码并不能直接看出什么。

因此这里转换思路：尝试让脚本跑起来，再通过 debug 查看内存值，看看能否找到密码。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B06%5D%20%5B15P%5D%20ELF%20-%20Fake%20Instructions/imgs/05.png)

------------

## 调试代码

在 Linux 通过 `gdb` 工具运行脚本，执行命令 `gdb crackme`  打开调试模式，

找到前面源码分析时的关键位置， 即 `WPA` 模块的 `call _strcmp` 方法：地址为 `0x80486f5` 。

执行命令 `break *0x80486f5` 在此处添加断点。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B06%5D%20%5B15P%5D%20ELF%20-%20Fake%20Instructions/imgs/06.png)

再执行命令 `r www.exp-blog.com` 开始调试代码，代码在断点位置中断。

由于此时正在调用 `strcmp` 函数，可以通过命令 `x/12wx $esp` 和 `x/s 地址值` 查看 esp 栈指针指向的函数内存值，借此检查真正的密码是否被传参到 `strcmp` 函数。

虽然可以找到其中的一个参数为输入的密码 `www.exp-blog.com` ，但是验证过另一个可疑的参数 `_0cGjc5m_.5\r\nÇ8CJ0À9` 并不是真正的密码，估计是经过某种加密处理的字符串。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B06%5D%20%5B15P%5D%20ELF%20-%20Fake%20Instructions/imgs/07.png)

------------

## 修改内存

此时我们剩下的途径就是查看 `blowfish` 分支会执行什么。

但是由于我们掌握不到正确的密码，因此无法令代码通过正常的途径走到 `blowfish` 分支。

不过我们可以直接修改内存达到我们的目的。

首先执行 `ni` 命令使得代码单步执行到 `test eax, eax` 语句，然后通过命令 `info reg` 查看当前所有寄存器的值，发现 `eax` 寄存器的值为 `0x1` 。

因为 `0x1 AND 0x1 = 0x1` ，所以在执行 `test eax, eax` 后 `ZF` 标志位会被置 1 ，即通过 `jnz` 或 `jne` 语句判定后都不会跳转到  `blowfish` 分支。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B06%5D%20%5B15P%5D%20ELF%20-%20Fake%20Instructions/imgs/08.png)

为了使得代码走向  `blowfish` 分支，此时我们只需要改变 `eax` 寄存器的值为 0 即可：

执行命令 `set $eax=0` ，再次通过命令 `info reg` 查看当前所有寄存器的值，发现 `eax` 寄存器的值被置为 `0x0` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B06%5D%20%5B15P%5D%20ELF%20-%20Fake%20Instructions/imgs/09.png)

此时直接执行命令 `c` 使得代码执行到最后就可以执行  `blowfish` 分支了，发现其作用就是打印真正的密码。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B06%5D%20%5B15P%5D%20ELF%20-%20Fake%20Instructions/imgs/10.png)

验证获得的密码 `liberté!` ，挑战成功。

> 注：这个密码直接提交到挑战即可，输入到脚本是没用的，因为根据前面分析可以知道，无论输入什么到这个脚本，均是判定密码错误。

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
