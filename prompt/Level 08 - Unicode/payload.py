#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 由于真正的 payload 里面存在不可见的 unicode 特殊字符 \u2028 (换行符)
# 因此这里使用 python 打印这个 payload
# 然后把打印的 payload 复制到题目注入点即可完成挑战

print('exp-payload:\u2028prompt(1)\u2028-->(after run, copy this line)')