## [[Root-Me](https://www.root-me.org/)] [[Cracking](https://www.root-me.org/en/Challenges/Cracking/)] [[ELF - Ptrace](https://www.root-me.org/en/Challenges/Cracking/ELF-Ptrace)] [[解题报告](http://exp-blog.com/2019/02/28/pid-3422/)]

------

## 前言

题目叫 Ptrace ，这个单词是 process 和 trace 的简写，直译为进程跟踪，但是这个翻译跟解题没半毛钱关系。。。

其实这题和【[Cracking : PE - 0 protection](https://github.com/lyy289065406/CTF-Solving-Reports/tree/master/rootme/Cracking/%5B03%5D%20%5B5P%5D%20PE%20-%200%20protection)】如出一辙，区别在于：

- 加了个壳
- 平台从 Windows 变成了 Linux

------------

## 试错

开启挑战后下载了文件 `ch3.bin` ，在 Linux 直接运行，随便输入一个密码，提示错误。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B07%5D%20%5B15P%5D%20ELF%20-%20Ptrace/imgs/01.png)

尝试使用 gdb 工具进行调试，执行命令 `gdb ch3.bin` 进入调试模式。

执行命令 `layout asm` 打印汇编源码，再执行命令 `r` 开始调试，但是程序并未按正常流程执行，而是直接报错：

`Debugger detecté ... Exit` （检测到调试器，退出程序）

很明显这程序被加壳了，看来要先找到加壳位置绕过去。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B07%5D%20%5B15P%5D%20ELF%20-%20Ptrace/imgs/02.png)

------------

## 源码分析

在 Windows 使用 IDA 打开文件 `ch3.bin` ，在 main 函数的入口附近发现这样的一块代码：

```asm
call    ptrace                  ; 这不是题目的提示么，，，原来是个壳。。。
add     esp, 10h
test    eax, eax                ; 测试寄存器 eax AND eax 的值 ，若结果为负数，SF=1 ， 反之 SF=0
jns     short loc_8048436       ; 当符号位 SF != 0 时跳转
```

不难发现 `jns` 的其中一个跳转分支是正常的代码执行模块，换言之另一个分支就是检测调试器的模块，亦即这就是加壳位置的入口。

那么要绕过也不难，在调试代码的时候，即时修改寄存器 eax 的内存值，改变 SF 符号位，从而诱导 `jns` 跳转到正常执行分支即可。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B07%5D%20%5B15P%5D%20ELF%20-%20Ptrace/imgs/03.png)


继续使用 IDA 分析其他部分的代码，通过 Search -> text ... 搜索前面运行代码时得到的关键字 `Wrong password` 。

直接就找到了判断输入密码是否正确的模块。

不难发现，这里做了 4 次连续比较，每次都是比较两个变量的值，只要其中一次 `al != dl` 则跳转到 `Wrong password` 分支。

```asm
cmp     dl, al
jnz     short loc_80484E4
```

由此可以推测：

- 程序是逐字符比较密码的
- 密码只有 4 个字符

那么只要在这 4 个位置做断点，就能把密码字符逐个找出来了。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B07%5D%20%5B15P%5D%20ELF%20-%20Ptrace/imgs/04.png)

------------

## 代码调试

回到 Linux 的 gdb 调试器，找到加壳位置 `ptrace` ，先加一个断点：`break *0x8048418`

在找到 4 个比较密码字符的位置，加 4 个断点：

- `break *0x80484a3`
- `break *0x80484b2`
- `break *0x80484bf`
- `break *0x80484ce`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B07%5D%20%5B15P%5D%20ELF%20-%20Ptrace/imgs/05.png)

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B07%5D%20%5B15P%5D%20ELF%20-%20Ptrace/imgs/06.png)

执行命令 `r` 开始调试，程序在第一个断点位置 `test eax, eax` 中断了。

输入命令 `info reg` 查看此时所有寄存器的值，发现 `eax = -1` 。

按照前面试错的流程，若继续向下执行， `test eax, eax` 会令符号位 `SF = 1` ，从而使得代码流转到 `Debugger detecté ... Exit` 的分支。

为了绕过它，此时可以直接执行命令 `set $eax=0` 修改寄存器的值，

这样执行 `test eax, eax` 语句之后就可以使得符号位 `SF = 0` ，从而流转到正常的代码分支了。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B07%5D%20%5B15P%5D%20ELF%20-%20Ptrace/imgs/07.png)

修改 eax 寄存器的值后，输入命令 `c` 继续执行代码，提示输入密码，说明我们成功绕过了加壳。

这里随便输入一个密码 `exp-blog.com` ，代码流转到下一个断点，即比较第一个密码字符的地方 `cmp %al, %dl` 。

不妨查看一下 `al` 和 `dl` 变量的值：

输入命令 `p/c $al` 查得 `al` 为字符 `e` ，输入命令 `p/c $dl` 查得 `dl` 也为字符 `e` 。

说明我的运气还是很好的，第一个密码字符蒙对了。

> `p/c` 命令解析：`p` 表示打印变量值，`c` 表示按字符格式输出。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B07%5D%20%5B15P%5D%20ELF%20-%20Ptrace/imgs/08.png)

输入命令 `c` 继续执行代码，代码流转到下一个断点，即比较第二个密码字符的地方 `cmp %al, %dl` 。

输入命令 `p/c $al` 查得 `al` 为字符 `a` ，输入命令 `p/c $dl` 查得 `dl` 为字符 `x` 。

这次运气就没那么好了，不过此时已经可以知道 `al` 存储的就是真正的密码，而 `dl` 存储的是我们输入的密码。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B07%5D%20%5B15P%5D%20ELF%20-%20Ptrace/imgs/09.png)

至此我们已经知道真正密码的前两个字符为 `ea` ，因此我们可以通过逐字符构造密码，重复前面的步骤，让程序不断流转到到下一个判断分支，从而获得完整的密码。

最终试出来的密码是 `easy` ，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B07%5D%20%5B15P%5D%20ELF%20-%20Ptrace/imgs/10.png)


------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
