## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[PHP preg_replace()](https://www.root-me.org/en/Challenges/Web-Server/PHP-preg_replace)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/web-server/php-preg-replace/)]

------


挑战的提示就是利用  PHP 的 `preg_replace()` 函数读取 `flag.php` 文件的源码。

------------

关于 `preg_replace()` 函数的语法定义，可以参考 [这里](http://www.runoob.com/php/php-preg_replace.html) ：

简单来说，这是正则替换函数，语法如下：

```php
/*
 *【函数定义】
 *  搜索 $subject 中匹配 $pattern 的部分， 以 $replacement 进行替换
 */
mixed preg_replace ( mixed $pattern , mixed $replacement , mixed $subject [, int $limit = -1 [, int &$count ]] )

/*
 *【参数说明】
 *  $pattern: 要搜索的模式，可以是字符串或一个字符串数组。
 *  $replacement: 用于替换的字符串或字符串数组。
 *  $subject: 要搜索替换的目标字符串或字符串数组。
 *  $limit: 可选，对于每个模式用于每个 subject 字符串的最大可替换次数。 默认是-1（无限制）。
 *  $count: 可选，为替换执行的次数。
 *
 *【返回值】
 *  如果 $subject 是一个数组， preg_replace() 返回一个数组， 其他情况下返回一个字符串。
 *  如果匹配被查找到，替换后的 $subject 被返回，其他情况下 返回没有改变的 $subject。
 *  如果发生错误，返回 NULL。
 */
```

------------

在本题中，用到的只有前 3 个参数 `$pattern` 、`$replacement` 、`$subject` ，最后的两个可选参数可无视掉。

开启挑战页面后，有三个输入框，每个输入框对应的参数如下：

- `search` => `$pattern`
- `replace` => `$replacement`
- `content` => `$subject`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B27%5D%20%5B30P%5D%20PHP%20preg_replace/imgs/01.png)

尝试输入正常的参数，发现页面输出了替换后的字符串，但是**会对特殊字符做过滤**，说明函数的输出不是利用点。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B27%5D%20%5B30P%5D%20PHP%20preg_replace/imgs/02.png)


------------

其实在正则表达式中是有多种模式的，如：

- `/i` 模式：不区分大小写
- `/g` 模式：全局匹配
- `/m` 模式：多行匹配
- `/e` 模式：**将替换串中的内容当作代码来执行**
- ......

其中 `/e` 模式是 PHP 语言特有的，这也是这题的解题关键。

关于 `preg_replace()` 函数漏洞的利用，可以参考 [这里](https://www.waitalone.cn/phpmyadmin-preg_replace-rce.html)。

简而言之，要触发 `preg_replace()` 漏洞有两个前置条件：

- 第一个参数 `$pattern` 需要 `/e` 模式，使得第二个参数 `replacement` 在替换前可以作为命令代码执行
- 第一个参数 `$pattern` 必能能够匹配到第三个参数 `subject` （否则 `preg_replace()` 函数会返回 `subject` 而不会执行 `replacement` 命令）

------------


例如构造这样的参数就**不会执行** `phpinfo()` 命令（因为 `/test/e` 不匹配 `just exp` ）：

`preg_replace('/test/e', 'phpinfo()', 'just exp');`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B27%5D%20%5B30P%5D%20PHP%20preg_replace/imgs/03.png)

而构造这样的参数就**可以执行** `phpinfo()` 命令（因为 `/test/e` 匹配 `just test` ）：

`preg_replace('/test/e', 'phpinfo()', 'just test');`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B27%5D%20%5B30P%5D%20PHP%20preg_replace/imgs/04.png)


------------

那么要读取 `flag.php` 文件，只需要把 `phpinfo()` 命令改成 `file_get_contents("flag.php")` 即可。

> `file_get_contents` 是 PHP 读取文件内容的函数。

亦即可以构造 payload 为：

- `search` => `/test/e`
- `replace` => `file_get_contents("flag.php")`
- `content` => `just test`

成功得到密码，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B27%5D%20%5B30P%5D%20PHP%20preg_replace/imgs/05.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
