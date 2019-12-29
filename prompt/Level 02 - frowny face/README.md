## [[prompt(1) to win](http://prompt.ml)] [[Level 2 - frowny face](http://prompt.ml/2)] [[解题报告](http://exp-blog.com/2019/03/18/pid-3626/)]

------

## 题目

```javascript
function escape(input) {
    //                      v-- frowny face
    input = input.replace(/[=(]/g, '');

    // ok seriously, disallows equal signs and open parenthesis
    return input;
}     
```

------------

## 解题报告

正则把输入内容中所有 `=` 和 `(` 过滤了。

 `=` 被过滤了不是什么大问题，XSS 直接放在 `<script>` 标签一样可以执行，关键是 `(` 被过略了。

此处可以利用 `<svg>` 标签【会对标签中的内容优先做实体编码解析】的原理进行绕过。

> 在网页编码中，以 `&#ASCII;` 称为实体编码，其中 ASCII 可以用十进制或十六进制表示。如 `(` 的 ASCII 编码为 40 （或十六进制 0x28） ，那么 `&#40;` 或 `&#x28;` 就是 `(` 的实体编码。

因此这题可构造这样的 payload 实现绕过：`<svg><script>prompt&#40;1)</script>` 。

它的工作原理为：

- 在 HTML 中，原本 `<script>` 标签属于 Raw text elements ，其内部文本遵循着不转义的规则。
- 但是 `<svg>` 标签属于 Foreign Elements ，即使在HTML语境下也不会受到 HTML 规则的影响，而是遵循 `<svg>` 自身的解析规则。
- 而 `<svg>` 直接继承自 XML，一般情况下，它的解析规则为：除非被 CDATA 包围，否则实体编码都会被转义。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2002%20-%20frowny%20face/imgs/01.png)


这题也可以利用 javascript 的 eval 函数实现绕过，payload 如下：

```javascript
<script>eval.call`${'prompt\x281)'}`</script>
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2002%20-%20frowny%20face/imgs/02.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
