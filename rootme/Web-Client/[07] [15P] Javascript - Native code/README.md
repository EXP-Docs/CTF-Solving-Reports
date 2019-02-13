## [[Root-Me](https://www.root-me.org/)] [[Cracking](https://www.root-me.org/en/Challenges/Web-Client/)] [[Javascript - Native code](https://www.root-me.org/en/Challenges/Web-Client/Javascript-Native-code)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2914/)]

------

水题，熟悉编码的样子就很容易做。

打开页面弹出了一个交互框，然后强制提交了，再报错 `fail` 。

打开浏览器开发者工具，切到 Network 找到名为 `ch16.html` 中的一段被混淆加密的 js 代码。

![](http://exp-blog.com/wp-content/uploads/2018/12/3bc164629dc0e35ebef0bcb14587bf5b.png)

虽然 js 有很多种混淆加密方式（JsFuck、aaencode、jjencode等），这些加密方式都有明显的识别特征。但是讲真，这题的加密方式我也是第一次看到，Google也找不到是什么类型的混淆加密（有些大神怀疑是[双重混淆](https://www.hackthissite.org/forums/viewtopic.php?f=28&t=11279)）。不过就算不知道加密方式，也可以直接利用浏览器去解码（不然浏览器就不能运行这段 js 了）。

复制这段混淆的 js 代码，打开浏览器开发者工具，切到 Console，粘贴进去，回车运行，发现出现了第2步的交互框。说明这是一个 function 函数，刚刚我们通过 Console 控制台调用他了，那么我们让控制台把这个 function 函数打印出来就相当于解码了。

![](http://exp-blog.com/wp-content/uploads/2018/12/271e0deb3e05bf8ddf4a482c6994141c.png)

再次黏贴这段混淆的 js 代码到 Console， 然后删除末尾的括号 `()` 使其丢失 function 的语义（也可以把末尾的 `()` 改成 `toString()`），回车运行，此时 Console 就打印了 function 函数原文了。

从 function 函数的 `if` 条件找到了密码，完成挑战。

![](http://exp-blog.com/wp-content/uploads/2018/12/bfabae67f32ca25df4bf8e7be73665d2.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
