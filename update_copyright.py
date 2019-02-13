#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os
import re


def find(root_dir, target_regex=r'', filter_regex=r'') :
    """
    在指定目录下(包括其子目录)查找满足要求的某些文件

    Args:
        root_dir: 被查找的目录
        target_regex: 所查找的目标文件名正则
        filter_regex: 过滤的文件名正则

    Returns:
        满足要求的文件列表(文件绝对路径)
    """

    find_list = list()
    file_list = os.walk(root_dir)    # 返回 root_dir 目录下所有目录和文件（包括子目录）

    for this, dirs, files in file_list:

        # for d in dirs: 
        #     if not re.match(filter_regex, d) :
        #         sub_dir = os.path.join(this, d)

        for f in files:
            if not re.match(filter_regex, f) and re.match(target_regex, f):
                file_path = os.path.join(this, f)
                find_list.append(file_path)

    return find_list



def update_copyright(file_list, bgn_year=2016, end_year=2099) :
    """
    更新文件内容中的 Copyright 起止年份信息

    Args:
        file_list: 文件列表(文件绝对路径)
        bgn_year: 起始年份
        end_year: 终止年份

    Returns:
        满足要求的文件列表(文件绝对路径)
    """

    for file_path in file_list :
        with open(file_path, 'r+') as file :
            lines = []
            end = False
            rpl = False

            while not end :
                line = file.readline()
                end = not line
                if re.search(r'Copyright \(C\).*', line) :
                    line = re.sub(r'\d+\-\d+', ('%i-%i' % (bgn_year, end_year)), line)
                    line = re.sub(r'\d+~\d+', ('%i~%i' % (bgn_year, end_year)), line)
                    rpl = True
                lines.append(line)

            if rpl :
                content = ''.join(lines)
                file.seek(0, 0)    # 由于读取操作导致指针已经移动到末尾，这里先把指针移动到文件头再覆盖写入（否则会变成追加内容）
                file.write(content)
                print('update: [%s]' % file_path)
    return



if __name__ == '__main__' : 
    file_list = find('/Users/exp/workspace/github/CTF-Solving-Reports', r'.*\.md$', r'^\..*')
    update_copyright(file_list, 2016, 2019)
    

            

