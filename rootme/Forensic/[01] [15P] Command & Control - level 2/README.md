## [[Root-Me](https://www.root-me.org/)] [[Forensic](https://www.root-me.org/en/Challenges/Forensic/)] [[Command & Control - level 2](https://www.root-me.org/en/Challenges/Forensic/Command-Control-level-2)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/forensic/command-&-control-level-2/)]

------

首先要知道这题的目标是需要在一个内存转存文件里面找到其所属**工作站的名称**。

开启挑战后会下载一个 `ch2.tbz2` 文件，解压后得到一个 500M 的 Windows 内存转存文件 `ch2.dmp`。有些同学可能不知道这个文件是如何打开并读取的，这里推荐使用的是 [volatility](https://github.com/volatilityfoundation/volatility) ，它是可以对 Windows 内存进行取证分析的工具。

volatility 的安装比较复杂，详细的安装和使用方法可以参考 [这里](https://www.freebuf.com/sectool/124690.html)。不过 volatility 已经被 Kali 收录了，我手上刚好装了 Kali 系统，就直接使用，不再安装了。

复制 `ch2.dmp` 到 Kali 的 `/tmp` 目录。在 `/tmp` 目录下执行命令 `volatility -f ch2.dmp imageinfo` ，可以根据查看该内存的系统镜像的摘要信息：

```bash
root@kali:/tmp# volatility -f ch2.dmp imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x86_23418, Win7SP0x86, Win7SP1x86
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : FileAddressSpace (/tmp/ch2.dmp)
                      PAE type : PAE
                           DTB : 0x185000L
                          KDBG : 0x82929be8L
          Number of Processors : 1
     Image Type (Service Pack) : 0
                KPCR for CPU 0 : 0x8292ac00L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2013-01-12 16:59:18 UTC+0000
     Image local date and time : 2013-01-12 17:59:18 +0100
```
从摘要信息 `Suggested Profile(s)` 可以知道 `volatility` 猜测这个 `dmp` 文件的数据结构可能源于三种 Windows 内核中的一个 （科普：不同版本的操作系统，其内核数据结构可能会发生改变，若不清楚 `profile` 则在提取 `dmp` 内容的时候可能会出错）。

这里任取一个 `profile` 尝试对 `ch2.dmp` 进行解析即可，例如 `Win7SP1x86`。

执行命令 `volatility -f ch2.dmp --profile=Win7SP1x86 envars` （其中 `envars` 参数表示查询所有进程的环境变量，更多的参数请指令可以自行搜索）：

```bash
root@kali:/tmp# volatility -f ch2.dmp --profile=Win7SP1x86 envars
Volatility Foundation Volatility Framework 2.6
Pid      Process              Block      Variable                       Value
-------- -------------------- ---------- ------------------------------ -----
     308 smss.exe             0x003b07f0 Path                           C:\Windows\System32
     308 smss.exe             0x003b07f0 SystemDrive                    C:
     308 smss.exe             0x003b07f0 SystemRoot                     C:\Windows
     404 csrss.exe            0x001c07f0 ComSpec                        C:\Windows\system32\cmd.exe
     404 csrss.exe            0x001c07f0 FP_NO_HOST_CHECK               NO
     404 csrss.exe            0x001c07f0 NUMBER_OF_PROCESSORS           1
     404 csrss.exe            0x001c07f0 OS                             Windows_NT
     404 csrss.exe            0x001c07f0 Path                           C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\
     404 csrss.exe            0x001c07f0 PATHEXT                        .COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC
     404 csrss.exe            0x001c07f0 PROCESSOR_ARCHITECTURE         x86
     404 csrss.exe            0x001c07f0 PROCESSOR_IDENTIFIER           x86 Family 6 Model 23 Stepping 6, GenuineIntel
     404 csrss.exe            0x001c07f0 PROCESSOR_LEVEL                6
     404 csrss.exe            0x001c07f0 PROCESSOR_REVISION             1706
     404 csrss.exe            0x001c07f0 PSModulePath                   C:\Windows\system32\WindowsPowerShell\v1.0\Modules\
     404 csrss.exe            0x001c07f0 SystemDrive                    C:
     404 csrss.exe            0x001c07f0 SystemRoot                     C:\Windows
     404 csrss.exe            0x001c07f0 TEMP                           C:\Windows\TEMP
     404 csrss.exe            0x001c07f0 TMP                            C:\Windows\TEMP
     404 csrss.exe            0x001c07f0 USERNAME                       SYSTEM
     404 csrss.exe            0x001c07f0 windir                         C:\Windows
     468 csrss.exe            0x004307f0 ComSpec                        C:\Windows\system32\cmd.exe
     468 csrss.exe            0x004307f0 FP_NO_HOST_CHECK               NO
     468 csrss.exe            0x004307f0 NUMBER_OF_PROCESSORS           1
     468 csrss.exe            0x004307f0 OS                             Windows_NT
     468 csrss.exe            0x004307f0 Path                           C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\
     468 csrss.exe            0x004307f0 PATHEXT                        .COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC
     468 csrss.exe            0x004307f0 PROCESSOR_ARCHITECTURE         x86
     468 csrss.exe            0x004307f0 PROCESSOR_IDENTIFIER           x86 Family 6 Model 23 Stepping 6, GenuineIntel
     468 csrss.exe            0x004307f0 PROCESSOR_LEVEL                6
     468 csrss.exe            0x004307f0 PROCESSOR_REVISION             1706
     468 csrss.exe            0x004307f0 PSModulePath                   C:\Windows\system32\WindowsPowerShell\v1.0\Modules\
     468 csrss.exe            0x004307f0 SystemDrive                    C:
     468 csrss.exe            0x004307f0 SystemRoot                     C:\Windows
     468 csrss.exe            0x004307f0 TEMP                           C:\Windows\TEMP
     468 csrss.exe            0x004307f0 TMP                            C:\Windows\TEMP
     468 csrss.exe            0x004307f0 USERNAME                       SYSTEM
     468 csrss.exe            0x004307f0 windir                         C:\Windows
     560 services.exe         0x001207f0 ALLUSERSPROFILE                C:\ProgramData
     560 services.exe         0x001207f0 CommonProgramFiles             C:\Program Files\Common Files
     560 services.exe         0x001207f0 COMPUTERNAME                   WIN-ETSA91RKCFP
     560 services.exe         0x001207f0 ComSpec                        C:\Windows\system32\cmd.exe
     560 services.exe         0x001207f0 FP_NO_HOST_CHECK               NO
     560 services.exe         0x001207f0 NUMBER_OF_PROCESSORS           1
     560 services.exe         0x001207f0 OS                             Windows_NT
     560 services.exe         0x001207f0 Path                           C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\
     560 services.exe         0x001207f0 PATHEXT                        .COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC
     560 services.exe         0x001207f0 PROCESSOR_ARCHITECTURE         x86
     560 services.exe         0x001207f0 PROCESSOR_IDENTIFIER           x86 Family 6 Model 23 Stepping 6, GenuineIntel
```
从返回信息可以找到一个变量名为 `COMPUTERNAME` ，其值就是工作站的名称，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Forensic/%5B01%5D%20%5B15P%5D%20Command%20%26%20Control%20-%20level%202/imgs/01.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
