## [[Root-Me](https://www.root-me.org/)] [[Cryptanalysis](https://www.root-me.org/en/Challenges/Cryptanalysis/)] [[Shift cipher](https://www.root-me.org/en/Challenges/Cryptanalysis/Shift-cipher)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/cryptanalysis/shift-cipher/)]

------

水题，题目就是提示，位移加密（其实就是凯撒加密）。

点击挑战后下载了一个 `ch7.bin` 文件，文件内容是乱码。

考虑到凯撒加密的特性，尝试对文件内容的每个字符的 ASCII 码做偏移，偏移范围从 `-256` 枚举到 `+256` 。

简单写了一段 python 代码实现，于是在偏移值为 -10 的时候，还原出了明文，得到密码，完成挑战。

代码比较简单，贴在下面：

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ch7.bin 的文件内容
ch7_bin = 'L|k€y+*^*zo‚*€kvsno|*k€om*vo*zk}}*cyvksr'

for offset in range(1, 256) :

	# ASCII码负向偏移
	try :
		pwd = ''
		for c in ch7_bin : 
			cn = chr(ord(c) - offset)
			pwd += cn
		print('offset=-%i, pwd=%s' % (offset, pwd))

	except Exception :
		pass # ascii overflow


	# ASCII码正向偏移
	try :
		pwd = ''
		for c in ch7_bin : 
			cp = chr(ord(c) + offset)
			pwd += cp
		print('offset=+%i, pwd=%s' % (offset, pwd))

	except Exception :
		pass # ascii overflow
```

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cryptanalysis/%5B05%5D%20%5B10P%5D%20Shift%20cipher/imgs/01.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
