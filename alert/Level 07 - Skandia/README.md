## [[alert(1) to win](https://alf.nu/alert1)] [[Level 07 - Skandia](https://alf.nu/alert1)] [[解题报告](http://exp-blog.com/2019/08/04/pid-3898/)]

------

## 题目

```javascript
function escape(s) {
  return '<script>console.log("' + s.toUpperCase() + '")</script>';
}
```

## 解题报告

这题用 `toUpperCase` 把输入字符全部转换成大写了。

JS 标签对大小写是不敏感的，但是 JS 函数则是大小写敏感，这样会导致 `alert()` 函数失效。

其实这种题型有通解：利用 `<svg>` 标签构做实体编码解析进行绕过。

> 在网页编码中，以 `&#ASCII;` 称为实体编码，其中 ASCII 可以用十进制或十六进制表示。如 `(` 的 ASCII 编码为 40 （或十六进制 0x28） ，那么 `&#40;` 或 `&#x28;` 就是 `(` 的实体编码。

其工作原理为：

- `toUpperCase` 对实体编码本身的字符（如 `&#97;`）进行大写转换，但是实体编码字符本身并没有对应的大写字符，因此不会起作用
-  `<svg>` 再把实体编码解析为对应的 ASCII 字符

因此这题可构造这样的 payload ：

```javascript
");</script><svg><img src=0 onerror=&#97;&#108;&#101;&#114;&#116(1); />
```


![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/alert/Level%2007%20-%20Skandia/imgs/01.png)



------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
