## [[Root-Me](https://www.root-me.org/)] [[Cracking](https://www.root-me.org/en/Challenges/Cracking/)] [[PE DotNet - 0 protection](https://www.root-me.org/en/Challenges/Cracking/PE-DotNet-0-protection)] [[解题报告](http://exp-blog.com/2019/02/26/pid-3409/)]

------

水题。

开启挑战后，下载了一个 `ch22.exe` 文件，运行后是一个 UI 程序。

随意输入一个 password ，点击 `Valider` 按钮后，提示密码错误。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B05%5D%20%5B10P%5D%20PE%20DotNet%20-%200%20protection/imgs/01.png)

使用 IDA 打开这个文件，尝试反汇编（注意使用 Microsoft.NET. assembly 方式打开）：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B05%5D%20%5B10P%5D%20PE%20DotNet%20-%200%20protection/imgs/02.png)

从左侧 `Function name` 可以找到 UI 程序每个组件模块的代码。

由于校验密码的行为是在我们点击按钮后触发的，因此可以猜测真正的密码被硬编码到这个点击行为的代码里面。

因此现在的目标应该是找到 `Valider` 按钮点击的事件代码。

而在 `Function name` 只有一个模块名为 `CrackMe.Form1__Button1_Click`，双击查看这个模块代码，可以发现这个模块调用了一个 `compare` 函数，而根据 `compare` 的结果，代码会流向两个分支，一个是验证密码失败，一个是验证密码成功，说明这就是目标代码。

不难注意到在 `compare` 函数前面有一个常量 `DotNetOP` ，很容易就会猜到这是硬编码到代码里面的真正密码。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B05%5D%20%5B10P%5D%20PE%20DotNet%20-%200%20protection/imgs/03.png)

尝试使用这个密码验证，挑战成功。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cracking/%5B05%5D%20%5B10P%5D%20PE%20DotNet%20-%200%20protection/imgs/04.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
