## [[prompt(1) to win](http://prompt.ml)] [[Level D – Json Object](http://prompt.ml/13)] [[解题报告](http://exp-blog.com/2019/03/27/pid-3737/)]

------

## 题目

```javascript
function escape(input) {
    // extend method from Underscore library
    // _.extend(destination, *sources) 
    function extend(obj) {
        var source, prop;
        for (var i = 1, length = arguments.length; i < length; i++) {
            source = arguments[i];
            for (prop in source) {
                obj[prop] = source[prop];
            }
        }
        return obj;
    }
    // a simple picture plugin
    try {
        // pass in something like {"source":"http://sandbox.prompt.ml/PROMPT.JPG"}
        var data = JSON.parse(input);
        var config = extend({
            // default image source
            source: 'http://placehold.it/350x150'
        }, JSON.parse(input));
        // forbit invalid image source
        if (/[^\w:\/.]/.test(config.source)) {
            delete config.source;
        }
        // purify the source by stripping off "
        var source = config.source.replace(/"/g, '');
        // insert the content using mustache-ish template
        return '<img src="{{source}}">'.replace('{{source}}', source);
    } catch (e) {
        return 'Invalid image data.';
    }
}
```

## 解题报告

### 前置知识

相当难的一道综合题型，考察对 Javascript 原理的理解程度，相关知识点如下：

- Object getter/setter 访问器（accessor）：[Object.prototype.\_\_proto\_\_](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object/proto)
- String 正则替换：[String.prototype.replace()](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/String/replace)

------------

### 代码分析

首先需要清楚代码逻辑，我们逐行分析下。

这里告知了我们输入的 `input` 格式只能为 JSON（不过 `data` 这个变量在本题是毫无用处的）：

```javascript
// pass in something like {"source":"http://sandbox.prompt.ml/PROMPT.JPG"}
var data = JSON.parse(input);
```

然后 `input` 会与一个固定的 JSON `{ 'source' : 'http://placehold.it/350x150' }` 执行 `extend` 操作。

这个 `extend` 函数看似复杂，但其实做的事情很简单：

检测 `input` 的 JSON **顶层**是否具有属性 `source` ，若有则不对 `input` 做任何修改。否则则在 `input` 的 JSON **顶层** 添加属性 `source` ，且取默认值为 `http://placehold.it/350x150` 。实际上这个函数是没什么用的。

处理后的 `input` JSON 对象存储到 `config` 变量中：

```javascript
var config = extend({
        // default image source
        source: 'http://placehold.it/350x150'
}, JSON.parse(input));
```

继而利用 `test` 函数正则校验 `config` JSON 对象的**顶层属性** `source` 的值，若其值含有 `0-9`、 `a-z`、 `A-Z`、 `_`、 `:`、 `/`、 `.`、 以外的字符，则删除 `source` 属性。

换言之这里是避免我们在**顶层属性** `source` 编写 payload 。

```javascript
// forbit invalid image source
if (/[^\w:\/.]/.test(config.source)) {
        delete config.source;
}
```

即使 `config` JSON 对象的**顶层属性** `source` 得以保留，也会把其中的双引号 `"` 全部过滤。

换言之这行代码是避免我们闭合 JSON 属性。

```javascript
// purify the source by stripping off "
var source = config.source.replace(/"/g, '');
```

最后把 `source` 的值作为 `<img>` 标签的 `src` 属性值输出到前端。

```javascript
// insert the content using mustache-ish template
return '<img src="{{source}}">'.replace('{{source}}', source);
```

大致的代码逻辑分析完毕，接下来可以开始寻找逻辑缺陷解题。

------------

### replace 正则绕过

由于过程略复杂，我们不妨从最终期望的目标开始，反向推导 payload 。

先不管前面代码逻辑如何，最后两行代码是：

```javascript
var source = config.source.replace(/"/g, '');
return '<img src="{{source}}">'.replace('{{source}}', source);
```

即我们所构造的 `source` 值，必须不含双引号 `"`，且能够触发 `prompt(1)` 事件。

当  `source`  是正常的图片 URL 时，不妨在浏览器控制台调试一下代码，看一下效果：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2013%20-%20Json%20Object/imgs/01.png)

正常情况下，如果要在 `<img>` 标签注入 JS ，一般是可以通过诸如 `<img src="0" onerror=prompt(1) >` 的方式。

但因为双引号 `"` 被过滤了，我们无法通过闭合 `src` 的双引号再增加 `onerror` 属性。

------------

但是根据 JS 的 [`replace('{{source}}', source)`](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/String/replace#%E8%AF%AD%E6%B3%95) 函数的语法，第二个由我们控制的参数 `source` 是可以插入**特殊变量名**以达到某些效果的（详见 [这里](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/String/replace#%E6%8F%8F%E8%BF%B0) ）：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2013%20-%20Json%20Object/imgs/02.png)

而我们要使用的特殊变量名，就是 

```
$`      // 这个变量名的效果是 【插入当前匹配的子串左边的内容】。
```

就这题而言，因为 `<img src="{{source}}">'.replace('{{source}}', source)` 第一个参数 `{{source}}` 匹配了原字符串，而所匹配部分的左边内容是 `<img src="`，因此若第二个参数 `source` 含有特殊变量，就会把 `<img src="` 插入到该特殊变量位置。 注意所插入的到 `<img src="` 最右侧刚好有一个双引号，那么我们就可以用来闭合 `src` 属性的双引号了。

于是我们可以构造 `source` 的值为 ：

```
$` onerror=prompt(1) >
```

当特殊变量被替换后，实际就等价于 `<img src=" onerror=prompt(1) >` ，再将其通过 `replace` 替换到原串的 `{{source}}` ，就可以得到：

```html
<img src="<img src=" onerror=prompt(1) >">
```

即 `src` 属性值等于 `"<img src="` ，被成功闭合了，同时因为是一个无效值，会触发到 `onerror` 的 JS 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2013%20-%20Json%20Object/imgs/03.png)


------------

### JSON 欺骗

那么接下来的问题就是，怎么保留我们所构造的 `source` 值到最后。

根据前面的分析知道， `source` 值就是源于我们输入的 json 的  `source` 属性值。

但是在此之前有这样的一段 `test` 代码，当 `source` 值含有 `0-9`、 `a-z`、 `A-Z`、 `_`、 `:`、 `/`、 `.`、 以外的字符，则删除 json 的 `source` 属性：

```javascript
// forbit invalid image source
if (/[^\w:\/.]/.test(config.source)) {
        delete config.source;
}
```

很不幸地，我们构造的 `source` 值是满足删除标准的。

换言之，若直接 input 的 JSON 如下，是无法把  `source`  属性值保留到最后的 :

```json
{ "source" : "$` onerror=prompt(1)" }
```


------------

最直接的想法是，能不能在 JSON 构造两个 `source` 属性骗过正则校验，使得其中一个没用的 `source`  被删除，而我们构造的 `source`  则得以保留。

不过问题是，JSON 是具备 hash 特性的，若直接**在同级构造两个同名属性** `source` ，后者是会覆盖前者的。

在浏览器控制台测试了一下，同名属性果然是会覆盖的：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2013%20-%20Json%20Object/imgs/04.png)

不过也并非一无所获，从控制台里面注意到，所构造的 JSON 对象具有一个隐藏属性 `__proto__` 。

------------


特意去查了一下这个属性的作用（详见 [这里](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object/proto)），得知在 JS 代码中，每个 JSON 对象都具有一个隐藏属性 `__proto__` ，而这个属性本质上是一个访问器，其作用是当我们需要访问 JSON 对象中的某个属性值时，可以提供类似于 `getter` / `setter` 访问方法的语法糖。

例如若在 JS 代码中定义一个这样的 JSON 变量 `var json = {"source": "exp"}` ：

- 当需要访问 `source` 的属性值时，如： `var src = json.source` ，实际上是 `__proto__` 的 `getter` 在起作用
- 当需要修改 `source` 的属性值时，如： `json.source = "EXP"` ，实际上是 `__proto__` 的 `setter` 在起作用

虽然 `__proto__` 是一个访问器，不过默认情况下，我们是不可以 `json.__proto__.source` 这样访问属性的。

但有趣的是，假如在 JSON 中**显式设置**了 `__proto__` 属性，例如这样：`{"__proto__": {"source": "exp"}}`

那么就会给 JS 解析器造成某些“混乱”，使得诸如 `json.__proto__.source` 的访问属性方式变成可能。

不但如此，此时 JSON 还同时支持 `json.source` 和 `json.__proto__.source` 两种访问属性方式，且他们是等价的：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2013%20-%20Json%20Object/imgs/05.png)

------------

利用这个特点，我们就可以在 JSON 的**同级构造两个同名属性**。

例如在 JS 中定义这样的一个 JSON 变量 `var json = {"source": "EXP", "__proto__": {"source": "M02"}}`

当 `"source": "EXP"` 属性存在时：

-  `json.source`  会优先得到 `EXP` 的值
-  `json.__proto__.source` 会得到全路径 `M02` 的值

当 `"source": "EXP"` 属性不存在时：

-  `json.source`  会通过 `__proto__` 访问器得到 `M02` 的值
-  `json.__proto__.source` 依旧会得到全路径 `M02` 的值

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2013%20-%20Json%20Object/imgs/06.png)

回到这题，我们可以利用这个 JSON 特性进行欺骗，在 input 构造一个类似这样的 JSON ：

`input = {"source": "--delete me--", "__proto__": {"source": "payload"}}`

其中第一个 `source` 只需要满足代码中 `test` 的正则条件使之被删除即可，这样第二个用于 payload 的 `source` 则可以保留到最后。


------------

### 完成挑战

结合前面所有分析，最终可以构造 payload 如下，完成挑战：

```json
{"source": "--EXP : Delete Me--", "__proto__": {"source": "$` onerror=prompt(1) >"}}
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2013%20-%20Json%20Object/imgs/07.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
