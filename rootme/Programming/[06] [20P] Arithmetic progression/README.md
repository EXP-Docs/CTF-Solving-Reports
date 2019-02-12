## [[Root-Me](https://www.root-me.org/)] [[Programming](https://www.root-me.org/en/Challenges/Programming/)] [[Arithmetic progression](https://www.root-me.org/en/Challenges/Programming/Arithmetic-progression-18)] [[解题报告](http://exp-blog.com/2019/02/09/pid-3255/)]

------

## 题目分析

高中数学题。

多刷新几次挑战页面可以得到一个规律，挑战给出了一条 **固定格式** 的 **递推公式** ：

$U_{n+1} = ( A + U_n ) \quad op \quad ( n * B )$

同时给出初值 $U_0$ ， 要求在 **2秒内** 求出当 $n$ 为某个数时，$U_n$ 的值。

其中：

- $A$ 和 $B$ 是一个随机整数，每次刷新页面都会变化
- $op$ 是一个运算符，只会是 $+$ 或 $-$
- $U_0$ 是随机整数，每次刷新页面都会变化
- $n$ 是随机正整数，每次刷新页面都会变化，且 $n$ 值较大

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Programming/%5B06%5D%20%5B20P%5D%20Arithmetic%20progression/imgs/01.png)

## 解题思路

直观的做法是直接从 $U_0$ 开始代入递推公式，一直循环计算，直到算出 $U_n$ 为止。

但是这是不可能的，因为题目所要求的 $n$ 值都很大，大到基本不可能在 2秒内 通过递推公式推算 $U_n$ 的结果。

因此正确的做法是，<font color="red">根据**递推公式**求出**通项公式**</font>，这是高中的 **数列** 知识。

## 求通项公式

求通项公式有很多种方法，这里使用 **累加法**， 求解过程如下：

对 $U_{n+1} = ( A + U_n ) \quad op \quad ( n * B )$ 变形得到：

$U_{n+1} - U_n = A \quad op \quad B * n$

逐项作差，于是有：

$$
\small{
\begin{cases}
U_n - U_{n-1} = A \quad op \quad B * ( n - 1 ) \\\
U_{n-1} - U_{n-2} = A \quad op \quad B * ( n - 2 ) \\\
U_{n-2} - U_{n-3} = A \quad op \quad B * ( n - 3 ) \\\
\text{...... } \\\
U_3 - U_2 = A \quad op \quad B * 2 \\\
U_2 - U_1 = A \quad op \quad B * 1 \\\
U_1 - U_0 = A \quad op \quad B * 0
\end{cases}
}
$$

对等号的左右两边分别相加，有：

　　$( U_n - U_{n-1} ) + ( U_{n-1} - U_{n-2} ) + ...... + ( U_2 - U_1 ) + ( U_1 - U_0 )$
　　$ = A * n \quad op \quad B * [(n - 1) + (n - 2) + (n - 3) + ... + 2 + 1 + 0]$

化简得：

$U_n - U_0 = A * n \quad op \quad B * \dfrac{(n-1)*n}{2}$

即通项公式为：

$U_n = A * n \quad op \quad B * \dfrac{(n-1)*n}{2} + U_0$

## 解题代码

得到通项公式，就可以在给定任意 $n$ 值的情况下，直接计算 $U_n$ 的值了。

因此代码只需要从挑战页面的 html 源码中抠取实时的 $A$、 $B$、 $op$、$U_0$ 、$n$ 的值，再将其直接代入通项公式计算 $U_n$ 即可。

详细代码如下：

> 注：此代码是用 python 3.5.2 写的，运行前需确保已在浏览器登陆了 rootme 并打开过此挑战页面

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import urllib.request
import http.cookiejar

CHARSET = 'utf-8'
ROOTME_URL = 'http://challenge01.root-me.org/programmation/ch1/'
POST_URL = 'http://challenge01.root-me.org/programmation/ch1/ep1_v.php?result=%s'


def main() :
    """
    主函数

    Returns:
        None
    """

    print('Init cookies ...')
    init_cookies()

    print('Get formula params ...')
    A, B, op, U0, n = get_params()
    print(' => A = %i' % A)
    print(' => B = %i' % B)
    print(' => op = %s' % op)
    print(' => U0 = %i' % U0)
    print(' => n = %i' % n)

    print('Calculate Un ...')
    Un = calculate(A, B, op, U0, n)
    print(' => Un = A * n %s B * n * (n - 1) / 2 + U0' % op)
    print(' => Un = %i' % Un)

    print('Sumbit Un ...')
    password = submit(Un)
    print(' => %s' % password)


def init_cookies() :
    """
    初始化 Cookie：
      从 PC 浏览器中提取 ROOTME_URL 相关的 Cookie 参数（需要人工先在浏览器登陆并打开一次 ROOTME_URL）

    Returns:
        None
    """

    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)
    return


def get_params() :
    """
    从挑战页面抠取实时参数值

    Returns:
        (A, B, op, U0, n)
    """

    A = None
    B = None
    op = None
    U0 = None
    n = None

    lines = urllib.request.urlopen(ROOTME_URL).readlines()
    for line in lines :
        html = line.decode(CHARSET)

        mth = re.compile(r' \= \[ (\S+) \+ U').search(html)
        if not A and mth :
            A = mth.group(1)

        mth = re.compile(r' \] ([\+\-]) \[ n \* (\S+) \]').search(html)
        if not B and mth :
            op = mth.group(1)
            B = mth.group(2)

        mth = re.compile(r'U<sub>0</sub> \= (\S+)').search(html)
        if not U0 and mth :
            U0 = mth.group(1)

        mth = re.compile(r'You must find U<sub>(\d+)').search(html)
        if not n and mth :
            n = mth.group(1)

    return int(A), int(B), op, int(U0), int(n)


def calculate(A, B, op, U0, n) :
    """
    把实时参数代入通项公式，计算第 n 项的值 Un

    Args:
        A: 通项公式的常量参数
        B: 通项公式的常量参数
        op: 通项公式的运算符
        U0: 通项公式的初值
        n: 期望计算的第 n 项

    Returns:
        数列中第 n 项的值 Un
    """

    if op == '+' :
        Un = A * n + B * n * (n - 1) / 2 + U0
    else :
        Un = A * n - B * n * (n - 1) / 2 + U0

    return int(Un)    # 结果必定是整数


def submit(Un) :
    """
    提交计算结果 Un

    Args:
        Un: 数列中第 n 项的值

    Returns:
        若没超时且验证码正确，则返回 CTF 密码
    """

    lines = urllib.request.urlopen(POST_URL % str(Un)).readlines()
    html = lines[0].decode(CHARSET)

    mth = re.match(r'.*?Congratz! The flag is : (\w+).*$', html)
    password = ('Success: %s' % mth.group(1)) if mth else ('Error or Timeout: %s' % html)
    return password



if __name__ == '__main__' :
    main()

```

代码的调用结果如下，页面提示 `Congratz` 说明完成挑战：

```python
# arithmetic_progression.py
Init cookies ...
Get formula params ...
 => A = 1
 => B = 21
 => op = +
 => U0 = 996
 => n = 931598
Calculate Un ...
 => Un = A * n + B * n * (n - 1) / 2 + U0
 => Un = 9112676903657
Sumbit Un ...
 => Success: lFablYE9P1

Process finished with exit code 0
```


------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2006~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
