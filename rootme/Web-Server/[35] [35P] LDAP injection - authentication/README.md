## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[LDAP injection - authentication](https://www.root-me.org/en/Challenges/Web-Server/LDAP-injection-authentication)] [[解题报告](http://exp-blog.com/2019/03/11/pid-3549/)]

------


## 前置知识

知道原理其实就是很水的一道题。

关于 LDAP 的前置知识可以参考这几篇文章：

- [LDAP Injection & Blind LDAP Injection](http://repository.root-me.org/Exploitation%20-%20Web/EN%20-%20Blackhat%20Europe%202008%20%20-%20LDAP%20Injection%20&%20Blind%20LDAP%20Injection.pdf)
- [LDAP注入与防御剖析](https://blog.csdn.net/quiet_girl/article/details/50716312)
- [LDAP注入漏洞与防御](https://www.jianshu.com/p/d94673be9ed0)


> 《[[CTF 解题报告] SQLi - LDAP.pptx](https://docs.google.com/presentation/d/e/2PACX-1vS7NmTzYRqKzR6WjqNFM1Ub0WHU0Gr3LKlwvLwAvJQUQRAd_-Q6RR68KVkEDjJgrlYvgUhbFxcz2p6A/pub?start=false&loop=false&delayms=3000)》



## 相关语法


这里简单解释一下， LDAP（Lightweight Directory Access Protocol，轻量级目录访问协议）其实就是**数据库的一种替代形式**，其原理是以目录树结构存储数据，不过它的语法比传统数据库要稍微简单一点。

与本题相关的一些 LDAP 语法：

- `WHERE A=xxx AND B=yyy` ，转变成 LDAP 语法就是 `(&(A=xxx)(B=yyy))`
- `WHERE A=xxx OR B=yyy` ，转变成 LDAP 语法就是 `(|(A=xxx)(B=yyy))`
- `WHERE A LIKE 'x%'` ，转变成 LDAP 语法就是 `(&(A=x*)(B=*))` 或 `(&(A=x*)(&))`（注：`(&)`是永真式）
- 支持嵌套，如： `(&(A=xxx)(|(A=xxx)(C=zzz)))`

> LDAP 把括号称之为【过滤器】，所有元素/操作都必须在括号内



## 找到注入点

知道这些就可以解题了。

注意题目要求是【**绕过登陆校验**】。

开启挑战后要求输入账号密码，因为知道是 LDAP ，那么就尝试闭合括号令其语法报错，看看会不会返回一些有用的异常信息。

输入探针 Username  = `admin)` ， Password = `123456` ，页面回显异常：

`ERROR : Invalid LDAP syntax : (&(uid=admin))(userPassword=123456))`

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B35%5D%20%5B35P%5D%20LDAP%20injection%20-%20authentication/imgs/01.png)

很明显，用于登陆验证的 LDAP 代码逻辑为：

`(&(uid=[username])(userPassword=[password]))`

其中 `[username]` 和 `[password]` 就是我们可控的注入点。



## 构造 payload

其实知道这两个注入点，绕过密码的注入方式就可以很灵活了（我至少想到了 5 种注入方法），关键是题目对 LDAP 的语法校验有多严格，这直接决定有效的 payload 数量。

------------

### 方法一：正确账号+嵌套式

构造 payload ：

- username = `账号)(|(uid=账号`
- password = `exp)`

实际拼接成的 payload 为：`(&(uid=账号)(|(uid=账号)(userPassword=exp)))`

这个 payload 先计算后面的 **或运算**，当 `账号` 正确的时候，由于 `(uid=账号)` 为真，所以无论 `userPassword` 输入任何值，整个条件式都是真，从而实现**密码绕过**。所以这个 payload 的**关键是找到正确的账号** （相比于猜密码，账号会更好猜）。

可以猜到的 `账号` 有 4 个：

- admin
- administrator
- root
- ch25 （这是从 URL 取到的题号，从 rootme 的经验上看，题号经常就是账号）

 逐个账号试，发现 `ch25` 果然就是账号，得到密码（回显被加密，需要看源码），完成挑战：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B35%5D%20%5B35P%5D%20LDAP%20injection%20-%20authentication/imgs/02.png)

------------

### 方法二：模糊匹配+嵌套式

相较于方法一，其实有另一个更巧妙的方法，可以构造这样的 payload ：

- username = `*)(|(uid=*`
- password = `exp)`

实际拼接成的 payload 为：`(&(uid=*)(|(uid=*)(userPassword=exp)))`

这个 payload 先计算后面的 **或运算**，而且由于 `(uid=*)` 是模糊匹配，必定永真（连账号也不用猜），所以无论 `userPassword` 输入任何值，整个条件式都是永真。

此方法在本题可以成功绕过验证，得到密码。

> 使用模糊匹配的前提是 `*` 没有被过滤，否则也是只能猜账号，但一般来说，账号比密码更好猜。

------------


### 方法三：永真式+解析器截断

构造 payload （此方式同样要求猜测正确的账号以绕过，由于已经知道是 `ch25` 就不猜了）：

- username = `ch25)(&)`
- password = `exp`

实际拼接成的 payload 为：`(&(uid=ch25)(&))(userPassword=exp))`

注意这个 payload 的前半部分 `(&(uid=ch25)(&))` 语法是正确的，但后半部分 `(userPassword=exp))` 因为括号没有配对，是语法错误的。

在某些对 LDAP 语法校验不严谨的题型，依然会从左到右执行，直到报错为止，因此这个 payload 在某些环境是可以实现绕过的。但是很明显这题不行：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B35%5D%20%5B35P%5D%20LDAP%20injection%20-%20authentication/imgs/03.png)

------------

### 方法四：永真式+%00截断

构造 payload （此方式同样要求猜测正确的账号以绕过，由于已经知道是 `ch25` 就不猜了）：

- username = `ch25)(&))%00`
- password = `exp`

实际拼接成的 payload 为：`(&(uid=ch25)(&))%00)(userPassword=exp))`

这与方法三很类似，只是截断依赖于 `%00` 而非解析器。

`%00` 是 C 或 PHP 的字符串终止符 `\0` 的 URL 编码，只要这个字符没有被过滤，在 LDAP 校验严谨的环境下也能对语法错误的 LDAP 进行截断。但是很明显这题不行：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B35%5D%20%5B35P%5D%20LDAP%20injection%20-%20authentication/imgs/04.png)


------------

### 方法五：串行过滤器

构造 payload （此方式同样要求猜测正确的账号以绕过，由于已经知道是 `ch25` 就不猜了）：

- username = `ch25)(uid=ch25)) (&(1=0`
- password = `exp`

实际拼接成的 payload 为：`(&(uid=ch25)(uid=ch25)) (&(1=0)(userPassword=exp))`

此方法构造了两个过滤器，在语法校验不严谨的 LDAP 中，只会执行第一个过滤器 `(&(uid=ch25)(uid=ch25))` ，而第二个过滤器 `(&(1=0)(userPassword=exp))` 则不会被执行，从而可以实现密码绕过。

而对于第一个过滤器，只要账号是正确的，就必定为真。不过此方式在本题也行不通：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B35%5D%20%5B35P%5D%20LDAP%20injection%20-%20authentication/imgs/05.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
