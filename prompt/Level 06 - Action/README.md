## [[prompt(1) to win](http://prompt.ml)] [[Level 6 - Action](http://prompt.ml/6)] [[解题报告](http://exp-blog.com/2019/03/22/pid-3664/)]

------

## 题目

```javascript
function escape(input) {
    // let's do a post redirection
    try {
        // pass in formURL#formDataJSON
        // e.g. http://httpbin.org/post#{"name":"Matt"}
        var segments = input.split('#');
        var formURL = segments[0];
        var formData = JSON.parse(segments[1]);

        var form = document.createElement('form');
        form.action = formURL;
        form.method = 'post';

        for (var i in formData) {
            var input = form.appendChild(document.createElement('input'));
            input.name = i;
            input.setAttribute('value', formData[i]);
        }

        return form.outerHTML + '                         \n\
<script>                                                  \n\
    // forbid javascript: or vbscript: and data: stuff    \n\
    if (!/script:|data:/i.test(document.forms[0].action)) \n\
        document.forms[0].submit();                       \n\
    else                                                  \n\
        document.write("Action forbidden.")               \n\
</script>                                                 \n\
        ';
    } catch (e) {
        return 'Invalid form data.';
    }
}
```

## 解题报告

题目代码还是挺好理解的：

- 输入内容以 `#` 分隔
- 左侧内容放入 `<form>` 的 `action` 属性
- 右侧内容是 json 格式，每一对 key-val 构造成 `<form>` 内的一个 `<input>` 子标签，其中 key 作为 `<input>` 的 `name` 属性值、val 作为 `<input>` 的 `value` 属性值
- 只要 `<form>` 的 `action` 属性值通过正则校验，则会调用 `<form>` 的 `submit()` 函数触发 `action` 行为

![](http://exp-blog.com/wp-content/uploads/2019/03/1340530308516c0123551d299f81b24b.png)

要在 `<form>` 的 `action` 属性执行 javascript 代码，可以构造这样的 payload：

`javascript:alert(1)#{"EXP":"M02"}`

但是由于 `document.forms[0].action` 的内容被正则过滤了，导致 `javascript:alert(1)` 无法执行：

![](http://exp-blog.com/wp-content/uploads/2019/03/d87bf0657e2f6bf0a216f05fc2e05b64.png)

但是这个过滤是不完善的，可以绕过。关键在于 `document.forms[0].action` 的指向。

当 `<forms>` 的子标签中没有任何名为 `<action>` 的子标签时， `document.forms[0].action` 指向的就是 `<forms>` 自身的 `action` 属性。

但若 `<forms>` 的子标签中，有任一子标签名为 `<action>` 时， `document.forms[0].action` 会优先指向该子标签。这样，正则过滤所校验的值就是子标签 `<action>` 的值，而非 `<forms>` 标签自身的 `action` 属性。

------------

回到此题，虽然题目会把我们输入的 json 构造成 `<form>` 内的 `<input>` 子标签，但是我们无法直接构造标签名为 `<action>` 。不过 json 的 key 会作为 `<action>` 标签的 `name` 属性值，而我们恰恰可以通过 `name` 属性为标签更名。

例如 `<input name="action">` 的名字实际是 action ，而非 input 。


------------

于是我们可以构造这样的 payload 绕过针对 action 的正则过滤：`javascript:alert(1)#{"action":"EXP"}`

显然成功触发了 alert 事件：

![](http://exp-blog.com/wp-content/uploads/2019/03/ccd55a34d3256026acf24ceeeebc0c84.png)

至此，只需要把 alert 改成 prompt 即可完成挑战，最终 payload 为：`javascript:prompt(1)#{"action":"EXP"}`

![](http://exp-blog.com/wp-content/uploads/2019/03/ca2e645438c16813d5624be1e9401dfd.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
