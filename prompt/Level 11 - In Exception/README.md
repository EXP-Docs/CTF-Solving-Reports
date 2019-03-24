## [[prompt(1) to win](http://prompt.ml)] [[Level B - In Exception](http://prompt.ml/11)] [[解题报告](http://exp-blog.com/2019/03/24/pid-3710/)]

------

## 题目

```javascript
function escape(input) {
    // name should not contain special characters
    var memberName = input.replace(/[[|\s+*/\\<>&^:;=~!%-]/g, '');

    // data to be parsed as JSON
    var dataString = '{"action":"login","message":"Welcome back, ' + memberName + '."}';

    // directly "parse" data in script context
    return '                                \n\
<script>                                    \n\
    var data = ' + dataString + ';          \n\
    if (data.action === "login")            \n\
        document.write(data.message)        \n\
</script> ';
}
```

## 解题报告

题目看上去似乎很复杂，其实可以简化成：

```html
<script>
    document.write('"Welcome back, ' + input + '."');
</script>
```

其中 `input` 是我们输入的内容，允许输入的字符只有 `a-z`、`A-Z`、`0-9`、`"`、`'`、`(`、`)` 。


------------

### JS 异常测试

这题其实很蹊跷，不清楚 Javascript 的异常机制很难成功解题。

不妨打开浏览器的控制台，输入这行 JS 代码：`document.write("fun"());`

留意异常信息为：`"fun" is not a function`

也就是说， JS 会把 `()` 前面的字符串识别是 函数名，但由于函数不存在，所以抛出异常。

![](http://exp-blog.com/wp-content/uploads/2019/03/b79e49a9cf70ba390b7cd6dfa9ffc9e3.png)

换言之， `()` 里面可能会被识别为函数的参数表，可以不妨再测试下。

先构造无效的参数，在控制台输入这行 JS 代码：`document.write("fun"(arg1, arg2));`

这次异常信息为：`arg1 is not defined` ，说明 `()` 里面确实被识别成参数表。

而且因为抛出的异常信息变成了参数异常，说明**参数表优先于函数名被解析**。

再构造有效的参数表测试一下：`document.write("fun"(1, "2", 3+4));`

这次异常信息又重新变成为： `"fun" is not a function`

![](http://exp-blog.com/wp-content/uploads/2019/03/34dbf351d9e73e6474a04721e72212be.png)

利用这个特性，如果参数表是函数调用、或表达式计算，那么就可以在抛出 `"fun" is not a function` 异常之前就先被执行了。

------------

### JS 异常利用

不妨构造这样的 JS 代码测试一下：`document.write("fun"(alert(1)));`

很明显，参数 `alert(1)` 会先被解析执行触发，在关闭 alert 窗口后，才抛出异常。

![](http://exp-blog.com/wp-content/uploads/2019/03/19cfebfef4506d6f64a49b4fb28d4f60.png)

![](http://exp-blog.com/wp-content/uploads/2019/03/f730eaf644c472e564070745206e7333.png)

这个特性或许可以用于解决这题。

在这题里，函数名 `fun` 就是 `Welcome back, ` ，而参数表是我们控制的，那么目标就是构造成这样的 JS 代码 ：

`document.write("Welcome back, "(prompt(1)));`

从运行结果上看，触发了 `prompt(1)` 执行，即这个方向是正确的。

据此我们就可以反推出 payload 应该为 `"(prompt(1))"` （注意要闭合双引号）

![](http://exp-blog.com/wp-content/uploads/2019/03/71a76aad3238a303af1674e34049f01c.png)

------------

### JS 操作符 in

但是这个 payload 还不足以解决问题，需要注意到，在我们注入点的后面，还有一个小尾巴 `.` 。

换言之，其实我们注入 `"(prompt(1))"` 这个 payload 后，得到的 JS 代码其实是这样的：

`document.write("Welcome back, "(prompt(1))".");`

而这个小尾巴最致命的地方，就是它先于参数表的 `prompt(1)` 被解析，导致先抛出了一个 `SyntaxError` 语法错误的异常， `prompt(1)` 则无法被执行。

![](http://exp-blog.com/wp-content/uploads/2019/03/aa0906fb08fb21166d51d31b36aec0d8.png)

那么接下来就需要处理掉这个语法错误的问题，使得参数表可以被解析。

但是由于 `+` 被过滤了，无法利用它拼接函数返回值和字符串去解决这个尾巴。

不过 JS 还有一个 `in` 操作符同样可以达到拼接目的，其使用方法是 `[a_object] in [b_object]` ，用于判断一个对象 a 是否被对象 b 包含。

虽然 `in` 对 object 类型有要求，但是即使是类型错误，也只会在运行时抛出，而不会在最开始解析时就直接报语法错误，从而可以解决前面语法错误导致参数表的 `prompt(1)` 没有被解析的问题。

![](http://exp-blog.com/wp-content/uploads/2019/03/d024a2d1b4aef46f0dd36849a8bf4948.png)

所以最终的 payload 为 `"(prompt(1))in"` ，构造成的 JS 代码为：

`document.write("Welcome back, "(prompt(1))in".");`

此 payload 运行时会依次触发 3 个事件：

- 解析并执行参数表的 `prompt(1)` （**已经足以完成挑战**）
- 抛出 `Welcome back, ` 函数未定义异常
- 抛出 `in` 操作符的 `TypeError` 异常

![](http://exp-blog.com/wp-content/uploads/2019/03/58b73117375cfd61693f7f600ac87071.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
