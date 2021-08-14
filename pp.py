# -*- coding: utf-8 -*-

import os
import shutil
import re
import random



HEAD = '''---
title: 【%(src)s】【%(type)s】 %(title)s
date: 2019-%(Mon)s-%(Day)s %(hh)s:%(mm)s:%(ss)s
categories: 
- CTF
tags:
- CTF
- %(src)s
- %(type)s
- 解题报告
---


- 来源：[%(src)s](%(src_url)s)
- 题型：[%(type)s](%(type_url)s)
- 题目：[%(title)s](%(title_url)s)
- 分数：%(point)s Points

'''

TAIL = '''


## 答案下载

- payload: [下载](%(payload_url)s)
- flag: [下载](%(flag_url)s)

> flag 下载后是名为 flagzip 的文件，需要手动更改文件后缀为 `*.zip`，然后解压即可（主要是为了避免 Root-Me 扫描）

'''


FILENAME = '[%(src)s][%(type)s] %(title)s'

def main() :
    DIR = '.'
    type = None
    for dirPath, dirNames, fileNames in os.walk(DIR):   #迭代目录
        if '.' == dirPath or '.git' in dirPath :
            continue

        if dirPath.startswith('./rootme/') :
            if re.match(r'\./rootme/[^/]+$', dirPath, flags=0) :
                rgx = r'\./rootme/([^/]+)$'
                ptn = re.compile(rgx)
                type = ptn.findall(dirPath)[0]
                try :
                    os.remove(dirPath + '/README.md')
                except :
                    pass

        if type is not None and dirPath.startswith('./rootme/' + type + '/') :
            if dirPath.endswith('imgs') :
                print(dirPath)
                continue

            if dirPath.endswith('src') or dirPath.endswith('testdata') or dirPath.endswith('doc') :
                continue

            srcpath = dirPath + '/README.md'
            with open(srcpath, 'r', encoding='utf-8') as file:
                data = file.read()

            # 替换首尾
            rgx = r'## \[\[([^]]+)\]\(([^]]+)\)\] \[\[([^]]+)\]\(([^]]+)\)\] \[\[([^]]+)\]\(([^]]+)\)\] \[\[([^]]+)\]\(([^]]+)\)\].*?------'
            ptn = re.compile(rgx, re.DOTALL)
            rst = ptn.findall(data)[0]
            point = re.search(r'./rootme/' + type + '/\[\d+\] \[(\d+)P\]', dirPath, flags=0)[1]

            _filename = FILENAME % {
                'src': rst[0], 
                'type': rst[2],
                'title': rst[4]
            }

            _head = HEAD % {
                'src': rst[0], 
                'src_url': rst[1], 
                'type': rst[2],
                'type_url': rst[3],
                'title': rst[4],
                'title_url': rst[5],
                'point': point,
                'Mon': str(random.randint(1, 12)).zfill(2), 
                'Day': str(random.randint(1, 28)).zfill(2), 
                'hh': str(random.randint(0, 23)).zfill(2), 
                'mm': str(random.randint(0, 59)).zfill(2), 
                'ss': str(random.randint(0, 59)).zfill(2)
            }
            data = re.sub(ptn, _head, data)


            if os.path.exists(dirPath + 'payload') :
                payload_url = './payload'
            else :
                payload_url = '#'

            if os.path.exists(dirPath + 'flagzip') :
                flag_url = './flagzip'
            else :
                flag_url = '#'

            _tail = TAIL % {
                'payload_url': payload_url, 
                'flag_url': flag_url
            }

            rgx = r'## 版权声明.*'
            ptn = re.compile(rgx, re.DOTALL)
            data = re.sub(ptn, _tail, data)


            # 替换图片
            rgx = r'\!\[\]\(.+?/imgs/'
            ptn = re.compile(rgx)
            data = re.sub(ptn, '![](./imgs/', data)

            
            # 保存文章
            args = dirPath.split('/')[:-1]
            snkdir = '/'.join(args) + '/' + _filename
            snkpath = snkdir + '.md'
            with open(snkpath, 'w+', encoding='utf-8') as file:
                file.write(data)

            # 迁移目录
            os.remove(srcpath)
            os.rename(dirPath, snkdir)
       



if __name__ == '__main__' :
    main()

