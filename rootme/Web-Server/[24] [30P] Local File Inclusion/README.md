## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[Local File Inclusion](https://www.root-me.org/en/Challenges/Web-Server/Local-File-Inclusion)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/web-server/localfileinclusion/)]

------

水题。关于 PHP 的 LFI 漏洞前置知识可以参考这篇文章： 【[Local File Inclusion (LFI) — Web Application Penetration Testing](https://medium.com/@Aptive/local-file-inclusion-lfi-web-application-penetration-testing-cc9dc8dd3601)】

但是不需要用到这些知识也能解题。


------------

开启挑战后，随意点击发现一个规律：

-  `| sysadm | reseau | esprit | crypto | coding | archives |` 页头的 tag 其实就是 【目录】
- 点击 tag 后出现的列表就是文件夹内的 【文件】或【子目录】
- 页面 URL 会随着点击变成 `http://challenge01.root-me.org/web-serveur/ch16/?files=目录&f=文件`
- 当点击【文件】时，会在页面输出文件内容

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B24%5D%20%5B30P%5D%20Local%20File%20Inclusion/imgs/01.png)

特别地，我发现如果点击【文件】后若没有输出文件内容，则这可能是【子目录】而非文件，

如： [http://challenge01.root-me.org/web-serveur/ch16/?files=crypto&f=archives](http://challenge01.root-me.org/web-serveur/ch16/?files=crypto&f=archives)

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B24%5D%20%5B30P%5D%20Local%20File%20Inclusion/imgs/02.png)

此时可以把页面路径中代表【文件】的 `f` （实际上是【子目录】）拼接到代表【目录】的 `files` 串成路径：

[http://challenge01.root-me.org/web-serveur/ch16/?files=crypto/archives](http://challenge01.root-me.org/web-serveur/ch16/?files=crypto/archives)

这样就可以查看【子目录】下的文件了：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B24%5D%20%5B30P%5D%20Local%20File%20Inclusion/imgs/03.png)

------------

题目要求找到 admin 的内容，但是在所有 tag 及其下的文件都没看见 admin 。

考虑到可能需要路径穿越，于是尝试构造 payload ：

`http://challenge01.root-me.org/web-serveur/ch16/?files=..`

得到上级目录下的文件列表，发现其中存在 `admin` ，但是点击后没有打印内容，怀疑 `admin` 其实是【子目录】：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B24%5D%20%5B30P%5D%20Local%20File%20Inclusion/imgs/04.png)


------------

于是构造新的 payload ：`http://challenge01.root-me.org/web-serveur/ch16/?files=../admin`

发现 `admin` 目录下的的 `index.php` 文件，打开后得到密码，完成挑战：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B24%5D%20%5B30P%5D%20Local%20File%20Inclusion/imgs/05.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
