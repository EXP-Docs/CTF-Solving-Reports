## [[Root-Me](https://www.root-me.org/)] [[App-System](https://www.root-me.org/en/Challenges/App-System/)] [[ELF x86 - Stack buffer overflow basic 1](https://www.root-me.org/en/Challenges/App-System/ELF32-Stack-buffer-overflow-basic-1)] [[解题报告](http://exp-blog.com/2019/01/14/pid-3002/)]

------

水题。

登录靶机后，在当前目录发现 3 个文件：

- .passwd ： 明显是目标文件，但是还没有权限打开
- ch13 ： 由 ch13.c 编译而成的脚本文件，且其 owner 具备 S 位权限
- ch13.c ： ch13 脚本的源文件，只是让我们看一下源码，知道其作用是当变量 `check==0xdeadbeef` 时，就帮当前用户进行提权

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/App-System/%5B01%5D%20%5B5P%5D%20ELF%20x86%20-%20Stack%20buffer%20overflow%20basic%201/imgs/01.png)

那么这题的切入点就在于如何令变量 `check` 的值变成 `0xdeadbeef` 实现当前用户提权，再读取 `.passwd` 文件。

首先来分析一下源码（分析要点我用注释进行标记了）：

```cpp
#include <stdlib.h>
#include <stdio.h>
 
/*
gcc -m32 -o ch13 ch13.c -fno-stack-protector
*/
 
 
int main()
{
 
  int var;
  int check = 0x04030201;		// 初始值是方便让我们对比有没有成功修改了 check 的值
  char buf[40];		// 注意到 数组buf 与 变量check 是相邻的，即它们的内存地址是连续的
 
  // 数组buf 长度只有 40，但这行代码却从标准输入流读取 45 个字符
  // 明显是在暗示可以通过 内存溢出 的方法覆写 变量check 的值
  fgets(buf,45,stdin);
 
  // 这两行输出是让我们确认 内存溢出 的结果的，真贴心
  printf("\n[buf]: %s\n", buf);
  printf("[check] %p\n", check);
 
  if ((check != 0x04030201) && (check != 0xdeadbeef))
    printf ("\nYou are on the right way!\n");
 
  if (check == 0xdeadbeef)
   {
     printf("Yeah dude! You win!\nOpening your shell...\n");
     system("/bin/dash");
     printf("Shell closed! Bye.\n");
   }
   return 0;
}
```

为了可以准确地通过 **内存溢出** 覆写变量 `check` ，首先需要知道 `fgets` 的特性，这是 API 说明：

```cpp
// fgets 会从  stream 读取 n-1 个字符存储到 s 指针指向的内存块，最后末尾自动补 \0
// 若 stream 的前 n-1 个字符中有换行符 \n，则读取到 \n （包括 \n），最后末尾自动补 \0
// 读取字符的数量只取决于这两个条件，与 s 指向的内存区（如数组）的长度无关
char *fgets 会从 (char *restrict s, int n, FILE *restrict stream);
```

回到这题，数组 `buf` 的长度是 40，而 `fgets` 读取的字符长度是 45，则可以构造如下的 payloads 先测试一下：

`0000000000000000000000000000000000000000abcd`

其中前 40 个字符 `0` 是用于填充数组 `buf` 的，后 4 个字符 ` abcd` 才是利用内存溢出覆写到变量 `check` 的真正的攻击载荷。

执行命令 `./ch13` 运行脚本，再输入这个 payloads ，最后按下回车输入 `\n` ，发现变量 `check` 的值被覆写了。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/App-System/%5B01%5D%20%5B5P%5D%20ELF%20x86%20-%20Stack%20buffer%20overflow%20basic%201/imgs/02.png)

进一步分析变量 `check` 的值，是 `0x64636261`，转换成 ASCII 码就是 `dcba`， 而所输入的 payloads 是 `abcd` ，顺序刚好相反。至此就有足够条件可以构造真正的 payloads 了。

从 `ch13.c` 的源码可以知道，变量 `check` 的目标值是 `0xdeadbeef` ，转换成 ASCII 就是 `Þ­¾ï` 。从测试 payloads 知道，顺序要逆转，因此真正的 payloads 就是：

`0000000000000000000000000000000000000000ï¾­Þ`

执行命令 `./ch13` 运行脚本，然后输入这个 payloads ，最后按下回车输入 `\n` ，发现变量 `check` 的值被成功覆写成 `0xdeadbeef` ， 同时也提权成功。

此时执行命令 `cat .passwd` 成功得到密码，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/App-System/%5B01%5D%20%5B5P%5D%20ELF%20x86%20-%20Stack%20buffer%20overflow%20basic%201/imgs/03.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
