## [[prompt(1) to win](http://prompt.ml)] [[Level 5 - Input Type](http://prompt.ml/5)] [[解题报告](http://exp-blog.com/2019/03/22/pid-3656/)]

------

## 题目

```javascript
function escape(input) {
    // apply strict filter rules of level 0
    // filter ">" and event handlers
    input = input.replace(/>|on.+?=|focus/gi, '_');

    return '<input value="' + input + '" type="text">';
}
```

## 解题报告

由于标签闭合 `>` 被过滤了，所以 js 只能通过标签属性触发。

其实 `type="text"` 就是个提示，input 标签可根据 type 改变自身为不同的元素类型，从而可以使用该类型的的属性触发 js 。

题目设定的默认类型是 text ，即输入框，这种类型可以触发 js 的属性只有 onfocus ，但是 focus 被过滤了，所以需要使用其他类型。

[查表](http://www.w3school.com.cn/tags/att_input_type.asp) 知道 input 的可用类型如下：

![](http://exp-blog.com/wp-content/uploads/2019/03/56de779e7dfde9213b8fa09c07220327.png)

**从中发现比较容易利用的类型是 button 和 image** 。


------------

假如要利用 button 按钮类型，可以通过 onclick 触发 js，期望结果是这样的 ：

`<input value="exp" type="button" onclick="prompt(1)" type="text">`

亦即 input 为 ： `exp" type="button" onclick="prompt(1)`

但是正则 `on.+?=` 过滤了 `onclick=`，不过这种过滤可以通过换行绕过，即构造 payload 为：

```html
exp" type="button" onclick
="prompt(1)
```

不过似乎是 BUG ，构造的按钮无法点击，导致无法触发 js。

![](http://exp-blog.com/wp-content/uploads/2019/03/e60fd2a05623c3b5f9dfeb22efb6797f.png)

------------

这样只能换个思路，利用 image 图片类型，通过 onerror 触发 js ，构造 payload 如下：

```html
exp" type="image" src=0 onerror
="prompt(1)
```

成功完成挑战。

![](http://exp-blog.com/wp-content/uploads/2019/03/491b2c70972afcf3f0c745b8a7fe5638.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
