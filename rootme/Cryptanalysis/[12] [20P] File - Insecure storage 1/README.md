## [[Root-Me](https://www.root-me.org/)] [[Cryptanalysis](https://www.root-me.org/en/Challenges/Cryptanalysis/)] [[File - Insecure storage 1](https://www.root-me.org/en/Challenges/Cryptanalysis/File-Insecure-storage-1)] [[解题报告](http://exp-blog.com/2019/03/02/pid-3445/)]

------

题目叫不安全的存储，要求我们找到用户的密码。

开启挑战后下载了一个 `ch20.tgz` 压缩包，解压后得到一个文件夹，从路径名来看应该是 firefox 浏览器的缓存文件。

在 `.mozilla\firefox\o0s0xxhl.default` 目录下找到很多 sqlite 数据库，使用 Navicat 逐个打开查看，发现只有 `signons.sqlite` 这个库存储了账密，但是都被加密过了，而且加密算法不明。

![](http://exp-blog.com/wp-content/uploads/2019/03/cc9e4904971dc14c852242cea66632f0.png)


------------

其实 firefox 浏览器会使用主密码去加密所访问的网页账密，然后缓存到本地 sqlite 数据库。

换言之如果我们持有主密码，是完全可以从缓存库恢复所有网页密码的。

而大多数情况下，只要不强制，就有很多人都没有设置主密码的意识。


------------

我从 Github 找到了 firefox 浏览器的缓存破解工具 【[firefox_decrypt](https://github.com/Unode/firefox_decrypt)】（其实这就是 POC 脚本）。

这个工具有一段说明是这样的：

```
Firefox Decrypt is a tool to extract passwords from Firefox/Thunderbird profiles.
It can be used to recover passwords from a profile protected by a Master Password as long as the latter is known. If a profile is not protected by a Master Password, a password will still be requested but can be left blank.
This tool does not try to crack or brute-force the Master Password in any way. If the Master Password is not known it will simply fail to recover any data.
```

翻译过来大概就是：

- Firefox Decrypt 是一个从 Firefox 缓存中提取密码的工具。
- 只要已知主密码，就可缓存中被主密码加密的密码。但若密码未受主密码保护，在使用此工具时可以不输入主密码。
- 此工具不会尝试以任何方式破解或暴力破解主密码。如果主密码未知，则无法恢复任何数据。


------------

虽然我们不知道挑战给我们的 firefox 缓存有没有主密码，但是抱着侥幸的心态，先试一下这个工具。

把 `ch20.tgz` 压缩包上传到 Linux ，解压得到 `.mozilla` 目录 （ firefox 缓存目录）。

然后上传 【[firefox_decrypt](https://github.com/Unode/firefox_decrypt)】的 `firefox_decrypt.py` 脚本到 Linux 。

执行命令 `python firefox_decrypt.py .mozilla/firefox/o0s0xxhl.default/`  (需安装 python2 以支持脚本运行)

运行过程中要求输入主密码，我们碰下运气看看是不是没有主密码，直接回车。

Bingo ! 得到密码，完成挑战。

![](http://exp-blog.com/wp-content/uploads/2019/03/688ca5aa7acb8a29caa43ddff4283f9f.png)


------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
