## [[prompt(1) to win](http://prompt.ml)] [[Level A - (╯°□°）╯︵ ┻━┻](http://prompt.ml/10)] [[解题报告](http://exp-blog.com/2019/03/24/pid-3706/)]

------

## 题目

```javascript
function escape(input) {
    // (╯°□°）╯︵ ┻━┻
    input = encodeURIComponent(input).replace(/prompt/g, 'alert');
    // ┬──┬ ﻿ノ( ゜-゜ノ) chill out bro
    input = input.replace(/'/g, '');

    // (╯°□°）╯︵ /(.□. \）DONT FLIP ME BRO
    return '<script>' + input + '</script> ';
}
```

## 解题报告

题目对输入内容**依次**做了三段过滤：

- 使用 `encodeURIComponent` 做 URL 编码
- 把 `prompt` 换成了 `alert`
- 过滤了所有单引号 `'`

虽然输入内容直接在 `<script>` 里面，但是要把 `prompt` 成功写入的方法似乎都失效了。

因为除了 `a-z`、 `A-Z`、`0-9`、 `.`、 `(`、 `)`、 `!`、 `~`、 `*` 这些字符，其他都几乎被过滤了。

------------


我起初期望使用这个 payload  `eval(String.fromCharCode(112,114,111,109,112,116,40,49,41)` 绕过 `replace` 以在前端直接构造 `prompt(1)` ，但是 `,` 被 `encodeURIComponent` 转码成了 `%2C` ，失败。。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2010%20-%20%28%E2%95%AF%C2%B0%E2%96%A1%C2%B0%EF%BC%89%E2%95%AF%EF%B8%B5%20%E2%94%BB%E2%94%81%E2%94%BB/imgs/01.png)

后来又想到，JS 解析器在解析标识符名称时（如函数名、属性名）等，若遇到 Unicode 会直接进行解码，并使得标识符依旧生效。于是又构造了这个 payload `\u0070\u0072\u006f\u006d\u0070\u0074(1)` 绕过 `replace` , 但是 `\` 被 `encodeURIComponent` 转码成了 `%5C` ，还是失败。。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2010%20-%20%28%E2%95%AF%C2%B0%E2%96%A1%C2%B0%EF%BC%89%E2%95%AF%EF%B8%B5%20%E2%94%BB%E2%94%81%E2%94%BB/imgs/02.png)


------------

其实这题想多了反而复杂，**可以利用题目自身的逻辑过滤去绕过**。

题目首先把 `prompt` 替换成 `alert` ， 然后又把单引号 `'` 替换成空。

那么其实只需要把单引号 `'` 插到 `prompt` 中间的任意位置就可以绕过所有过滤了。。。

所以这些 payload 都是可以完成挑战的：

- `p'rompt(1)`
- `pr'ompt(1)`
- `pro'mpt(1)`
- `prom'pt(1)`
- `promp't(1)`
- `p'r'o'm'p't(1)`

因为这些字符本身属于保留字符，不会被 `encodeURIComponent` 编码；其次 `prompt` 中间有单引号 `'` 的时候，也不满足 `replace` 的条件；最后题目还很贴心地帮我们把所有单引号 `'` 删掉了，，，，所以有时其实真是我们想太多了。。。(╯°□°）╯︵ ┻━┻

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2010%20-%20%28%E2%95%AF%C2%B0%E2%96%A1%C2%B0%EF%BC%89%E2%95%AF%EF%B8%B5%20%E2%94%BB%E2%94%81%E2%94%BB/imgs/03.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
