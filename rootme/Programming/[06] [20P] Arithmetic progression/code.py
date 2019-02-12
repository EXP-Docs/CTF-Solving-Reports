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
