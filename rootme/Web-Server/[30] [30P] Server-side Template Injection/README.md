## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[Server-side Template Injection](https://www.root-me.org/en/Challenges/Web-Server/Server-side-Template-Injection)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/web-server/server-side-template-injection/)]

------


## 前置知识

SSTI (服务侧模板注入) 题型，此挑战要用到的相关知识可以参考以下文档：

- [服务端模板注入攻击 （SSTI）之浅析](https://www.freebuf.com/vuls/83999.html)
- [SSTI攻击分析](https://hellohxk.com/blog/ssti/)
- [FreeMarker执行系统命令](https://yq.aliyun.com/articles/519369)
- [freemarker学习笔记---assign标签](https://blog.csdn.net/yin767833376/article/details/51831262?utm_source=blogxgwz0)

------

## 试错

题目要求是读取文件【SECRET_FLAG.txt】的内容。

开启挑战后只有一个输入框，首先试试能不能 XXS ，输入一个探针 `<img src=0 />` ，发现原文回显，即被过滤了：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B30%5D%20%5B30P%5D%20Server-side%20Template%20Injection/imgs/01.png)

然后尝试直接访问 【[http://challenge01.root-me.org/web-serveur/ch41/SECRET_FLAG.txt](http://challenge01.root-me.org/web-serveur/ch41/SECRET_FLAG.txt)】，理所当然报错：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B30%5D%20%5B30P%5D%20Server-side%20Template%20Injection/imgs/02.png)

------

## SSTI 探针

既然这些方法都被封锁了，题目有提示是要用 SSTI 解题，还是不绕弯子实打实做吧~~

但是要使用 SSTI 攻击，首先需要知道这个页面使用了什么模板引擎。

在 [网上](https://www.freebuf.com/vuls/83999.html) 找到了 Burp Sutie 提供的一套 payload探针，用于快速确认模板引擎（其中绿色分支表示探针注入成功时的下一个步骤，红色表示注入失败时的下一个步骤）：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B30%5D%20%5B30P%5D%20Server-side%20Template%20Injection/imgs/03.png)

根据流程按部就班做就可以了。首先输入探针 `${7*7}` ，发现 WEB 计算成了 `49` ，即注入成功：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B30%5D%20%5B30P%5D%20Server-side%20Template%20Injection/imgs/04.png)

继续输入下一个探针 `a{*comment*}b` ，这次原文回显，即注入失败：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B30%5D%20%5B30P%5D%20Server-side%20Template%20Injection/imgs/05.png)

继续输入下一个探针 `${"z".join("ab")}` ，这次直接返回异常，即注入失败。

从探针流程上看，我们测试得到的模板引擎是 `Unknown` 。。。

不过仔细观察返回的异常信息，可以看见信息 `freemarker` 。

从网上找到 freemarker 是属于 Java 语言的模板引擎，因此可以针对性进行注入。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B30%5D%20%5B30P%5D%20Server-side%20Template%20Injection/imgs/06.png)

------

## 构造 payload

由于题目目标很明确要我们读取文件【SECRET_FLAG.txt】的内容，因此很自然就想到最直接的方法就是使用 **系统命令** 读取这个文件，例如：`cat SECRET_FLAG.txt` 。

接下来只需要找到方法“如何通过 freemarker 调用系统命令”即可。

我稍微找了一下就看到了 [这篇文章](https://yq.aliyun.com/articles/519369) ，它提供的 payload 还是很简单的：

```
<#assign exp="freemarker.template.utility.Execute"?new()>
${exp("any system cmd")}
```

其中第一行的意思是：利用 `assign` 标签定义一个全局变量 `exp` ，这个全局变量是通过 `freemarker.template.utility.Execute` 类 `new` 出来的一个实例变量。而在 freemarker 中， `freemarker.template.utility.Execute` 类的功能是调用系统命令。

第二行的意思就更简单了：利用全局变量 `exp` 调用任意系统命令。

> 关于 freemarker 的 `assign` 标签的功能可以参考 [这篇文章](https://blog.csdn.net/yin767833376/article/details/51831262?utm_source=blogxgwz0) 。

我们可以通过一个简单的 Linux 系统命令 `id` 测试它是否起作用，构造 payload 如下（**去掉了换行**）：

`<#assign exp="freemarker.template.utility.Execute"?new()>${exp("id")}`

成功获取到了当前 Linux 用户的 id 信息。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B30%5D%20%5B30P%5D%20Server-side%20Template%20Injection/imgs/07.png)

------

## 完成挑战

于是可以开始解题了，首先查看一下 SECRET_FLAG.txt 文件在哪，构造 payload 如下：

`<#assign exp="freemarker.template.utility.Execute"?new()>${exp("ls -al")}`

很幸运地，这个文件就在当前目录：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B30%5D%20%5B30P%5D%20Server-side%20Template%20Injection/imgs/08.png)

最后我们构造 payload 读取这个文件：

`<#assign exp="freemarker.template.utility.Execute"?new()>${exp("cat SECRET_FLAG.txt")}`

得到 flag ，完成挑战：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B30%5D%20%5B30P%5D%20Server-side%20Template%20Injection/imgs/09.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
