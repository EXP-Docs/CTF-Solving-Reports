## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[Backup file](https://www.root-me.org/en/Challenges/Web-Server/Backup-file)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2960/)]

------

这题全靠猜。题目声明了 `No clue` ，从各个方向找确实也没有什么信息。

最开始想到用 Burp Suite -> Intruder 或者 hydra 做登录账密爆破，但是无果，应该不是弱密码。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B06%5D%20%5B10P%5D%20Backup%20file/imgs/01.png)

其实题目本身就是提示：`Backup file`（备份文件）。

换个角度想，可能这个 web 服务的某个文件的备份，曾经写入过账密信息，需要找出这个备份文件。

于是又测试了命令注入，尝试打印目录列表，无果。

再换个角度想，可能是某种工具编辑文件后**自动生成的文件备份**，需要去猜这个备份文件的名称。但**首先需要猜这个被编辑的文件**是什么，**才能猜它的备份文件名**。

首先想到被编辑的是首页，直接在 URL 末尾补 `index.***` 测试首页文件名，除了 `index.php` 之外都是跳到 404，这样就确定了首页文件名了。

然后再猜常见的备份后缀 `index.php.bak`、 `index.php_bak`、`index.php-bak` 等等也都是跳到 404 。

后来想了想， web 服务一般都是在 linux 系统的， linux 常用的文本编辑器是 vim， 而 **vim 开启自动备份后，备份文件的后缀是波浪号** `~` 。

于是尝试在 URL 末尾补 `index.php~` ， Bingo !!! 下载了该备份文件，打开之后找到了密码，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B06%5D%20%5B10P%5D%20Backup%20file/imgs/02.png)
![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B06%5D%20%5B10P%5D%20Backup%20file/imgs/03.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
