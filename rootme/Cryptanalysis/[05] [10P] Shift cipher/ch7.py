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
