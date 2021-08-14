## [[Root-Me](https://www.root-me.org/)] [[Cracking](https://www.root-me.org/en/Challenges/Cracking/)] [[ELF - CrackPass](https://www.root-me.org/en/Challenges/Cracking/ELF-CrackPass)] [[解题报告](http://exp-blog.com/2019/03/01/pid-3434/)]

------


## 前言

【[Cracking : ELF - Ptrace](https://github.com/lyy289065406/CTF-Solving-Reports/tree/master/rootme/Cracking/%5B07%5D%20%5B15P%5D%20ELF%20-%20Ptrace)】的进阶版，区别在于：无法从静态源码中查看代码地址了~

其实除了不方便打断点之外，逆向流程还是一样的，不算太难。

不过两题的知识点还是共通的，建议先做【[Cracking : ELF - Ptrace](https://github.com/lyy289065406/CTF-Solving-Reports/tree/master/rootme/Cracking/%5B07%5D%20%5B15P%5D%20ELF%20-%20Ptrace)】。

------------

## 试错

开启挑战后下载压缩包 `ch8.zip` ，解压后得到脚本 `Crack` 。

放到 Linux 上直接运行，发现给定不同的密码有不同的提示：

- 若无密码，如执行命令 `./Crack`， 提示 `You must give a password for use this program !`
- 若密码有特殊字符，如执行命令 `./Crack exp-blog.com`， 提示 `Bad password !`
- 若密码无特殊字符，如执行命令 `./Crack exp`， 提示 `Is not the good password !`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B14%5D%20%5B30P%5D%20ELF%20-%20CrackPass/imgs/01.png)


执行命令 `gdb Crack` 开启调试器，但是输入命令 `layout asm` 后却没有显示汇编源码。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B14%5D%20%5B30P%5D%20ELF%20-%20CrackPass/imgs/02.png)

执行命令 `r` 开始调试代码，此时才显示汇编源码，但是提示 `Don't use a debuguer !` 。

至此我们获得三个信息：

- 源码地址只有在代码运行时才能查看，增加了打断点调试的难度
- 程序被加壳了，需要绕过调试器检测
- 一个常量字符串  `Don't use a debuguer !`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B14%5D%20%5B30P%5D%20ELF%20-%20CrackPass/imgs/03.png)

------------

## 绕过壳

由于我们看不到代码的静态地址，因此就无法在 `Don't use a debuguer !` 之前打断点进行绕过，此时要换个思路。

输入命令 `info file` 可以列出文件每个段的入口地址，其中 `.text` 是代码段的入口，亦即 main 函数的入口。

可以看到代码段的地址范围为 `0x08048440 - 0x0804877c`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B14%5D%20%5B30P%5D%20ELF%20-%20CrackPass/imgs/04.png)

执行命令 `break *0x08048440` 在入口地址打个断点，然后输入命令 `r exp` 开始调试 。

> 此处随便使用一个无特殊字符的密码 `exp` ，是为了绕过 `Bad password !` 分支，后面用 IDA 一看源码时就知道为什么要这样做了。此处直接用无特殊字符的密码只是为了简化调试过程。

明显程序在入口位置中断了，我们看到了 main 函数入口 `__libc_start_main@plt` ，且还没有提示 `Don't use a debuguer !` ，说明我们在检测点之前刹车了。问题是，检测点在哪 ？

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B14%5D%20%5B30P%5D%20ELF%20-%20CrackPass/imgs/05.png)

此时同步在 Windows 下用 IDA 打开 `Crack` 文件。

找到 `main` 函数的代码附近有一个 `jns short loc_804869F` 跳转语句 （补全地址为 `0x0804869F`），该语句的其中一个分支就是 `Don't use a debuguer !` 。

因此现在的目标就是在 Linux 的 dbg 下找到这个位置进行绕过。

在 dbg 下通过键盘 `↓` 滚动代码，很快找到 `jns 0x804869f` 语句，由于这是要绕过的语句，因此在其前一条语句 `test %eax,%eax` 打断点。

因其地址为 `0x804868a` ，输入命令 `break *0x804868a` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B14%5D%20%5B30P%5D%20ELF%20-%20CrackPass/imgs/06.png)

执行命令 `c` 让代码继续运行，在语句 `test %eax,%eax` 处中断。

此时输入命令 `info reg` 查看寄存器 eax 的值为，得知为 -1 。

若如常执行，由于 test 的结果为负数，即 SF 符号位会被置 1 ，`jns` 判断后必定会流转到 `Don't use a debuguer !` 分支。

要改变分支走向，就需要在此时通过修改寄存器 eax 的值，间接改变 SF 符号位。

输入命令 `set $eax=0` 即可绕过。

------------

## 找到密码

修改寄存器后，先不忙着执行代码，否则即使绕过了 debuguer 判定，由于密码是错的，程序还是会直接执行到 `Is not the good password !` 的分支。

现在的目标是找到密码判定的位置，让程序中断在那里。

从 IDA 查看代码，接下来应该是会流转到 `call sub_80485A5` 模块，双击可以跳转到这个模块。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B14%5D%20%5B30P%5D%20ELF%20-%20CrackPass/imgs/07.png)

在这个模块里，很快就发现 `call _strcmp` 语句，以及其后的正确 / 错误密码的分支。

> 虽还有一个 `Bad password !` 分支，但综合前面分析已经知道，因为这次调试输入的密码没有特殊字符，所以不用管这个分支。

唯一的问题是，没有这个语句的地址，不能直接打断点。

但是我们找到在其前面不远处的子模块入口地址 `loc_80485E8` ，即 `0x080485E8` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B14%5D%20%5B30P%5D%20ELF%20-%20CrackPass/imgs/08.png)

回到 Linux 的 gdb ，输入命令 `break *0x080485E8` 打上断点，然后执行命令 `c` 让程序继续运行。

此时从 gdb 的源码已经可以直接看到密码比较语句 `call 0x804842c <strcmp@plt>` 了，其地址为 `0x8048617` 。

执行命令 `break *0x8048617`  在此处打上断点，然后执行命令 `c` 让程序运行到此处。

剩下的事情就简单，只需要查看比较函数 `strcmp` 的两个入参即可，必定有一个是正确密码。

须知道函数是存储在栈空间的，而栈指针为 esp ，因此先执行命令 `x/8wx $esp` 可以查到 esp 指针所指向栈顶的前 8 个地址。

在通过 `x/s 地址` 命令逐个地址查看，发现前两个地址就是 `strcmp` 函数入参。

其中一个是输入的密码，另一个是真正的密码，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B14%5D%20%5B30P%5D%20ELF%20-%20CrackPass/imgs/09.png)

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B14%5D%20%5B30P%5D%20ELF%20-%20CrackPass/imgs/10.png)


------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
