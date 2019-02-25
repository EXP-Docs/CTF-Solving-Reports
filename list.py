
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

        for d in dirs: 
            if not re.match(filter_regex, d) :
                sub_dir = os.path.join(this, d)

        for f in files:
            if not re.match(filter_regex, f) and re.match(target_regex, f):
                file_path = os.path.join(this, f)
                find_list.append(file_path)

    return find_list



if __name__ == '__main__' : 
    # file_list = find('D:\\workspace\\Github\\CTF-Solving-Reports\\rootme\\App-System', r'.*\.md$', r'^\..*')
    # print(file_list)

    ctype = 'Web-Server'
    fdir = 'D:\\workspace\\Github\\CTF-Solving-Reports\\rootme\\%s\\' % ctype
    sfiles = os.listdir(fdir)

    index = ""
    point = ""
    challenge = ""
    challenge_link = ""
    solve = ""
    solve_link = ""

    kv = {}
    fMD = fdir + '\\README.md'
    with open(fMD, 'r', encoding='utf-8') as md :
        line = md.readline()
        while line :
            mth = re.match(r'\- \S+ ([^\]]+)\]\((.*?)\).*', line)
            if mth :
                key = mth.group(1)
                val = mth.group(2)
                kv[key] = val
            line = md.readline()

    for sfile in sfiles:
        if re.match(r'.*\.md$', sfile) :
            pass

        else :
            mth = re.match( r'\[(\d+)\] \[(\d+P)\] (.*)', sfile)
            if mth :
                index = mth.group(1)
                point = mth.group(2)
                challenge = mth.group(3)

                with open(fdir + '\\' + sfile + '\\README.md', 'r', encoding='utf-8') as file :
                    line = file.readline()
                    ary = line.split(')] [[')
                    challenge_link = ary[2].split('](')[1]
                    solve_link = ary[3].split('](')[1].split(')]')[0]
                    solve_link = kv[challenge]

                tmp = '\n'.join([
                    '      <tr> ', 
                    '       <td>%s</td> ', 
                    '       <td>%s</td> ', 
                    '       <td><a href="%s">%s</a></td> ', 
                    '       <td><a href="%s">Solving Report</a></td> ', 
                    '       <td>None</td> ', 
                    '       <td><a href="%s/flag">Flag</a></td> ', 
                    '       <td>%s</td> ', 
                    '      </tr> '
                ]) % (ctype, index, challenge_link, challenge, solve_link, solve_link, point)    
                print(tmp)