## [[Root-Me](https://www.root-me.org/)] [[Programming](https://www.root-me.org/en/Challenges/Programming/)] [[Quick Response Code](https://www.root-me.org/en/Challenges/Programming/Quick-Response-Code)] [[解题报告](http://exp-blog.com/2019/02/10/pid-3267/)]

------

## 题目分析

与 [CAPTCHA me if you can](https://www.root-me.org/en/Challenges/Programming/CAPTCHA-me-if-you-can) 是相同的题型，都是图像识别，不过这题更简单。这题需要识别的是二维码，而且识别限时增加到 6 秒。




多刷新几次页面可以发现，题目给出的二维码是缺损的，不过所缺损的必定是在二维码 **左上、右上、左下** 的三个“回”形图案。

这三个“回”形图案是所有二维码都必须有的，其作用是用于扫描定位。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Programming/%5B09%5D%20%5B40P%5D%20Quick%20Response%20Code/imgs/01.png)


## 二维码分析

随便下载一个二维码，添加辅助线进行分析，可以得到几个信息：

- 二维码宽高为 300x300
- 二维码的每一个大像素点，实际上是由 9x9 的原子像素构成的
- 二维码距离边沿为两个大像素点，即 18 个原子像素的距离
- “回”形图案的外圈大小为 7x7 个大像素点，内圈为 3x3 个大像素点，镂空距离为 1 个大像素点
- 以原子像素计算，三个缺失的“回”形图案的左上角顶点坐标分别为 (18, 18)、 (18, 216)、 (216, 18)

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Programming/%5B09%5D%20%5B40P%5D%20Quick%20Response%20Code/imgs/02.png)

## 二维码修复

知道这些信息，就可以修复二维码了：

- 以  (18, 18)、 (18, 216)、 (216, 18) 三个坐标为起点，分别画一个黑色矩形，矩形大小为 7x7 个大像素点（外圈）
- 从三个坐标起点向右下方向位移 1 个大像素点，分别画一个白色矩形，矩形大小为 5x5 个大像素点（镂空区域）
- 从三个坐标起点向右下方向位移 2 个大像素点，分别画一个黑色矩形，矩形大小为 3x3 个大像素点（内核）

> 注：一个大像素点 = 9x9 个原子像素

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Programming/%5B09%5D%20%5B40P%5D%20Quick%20Response%20Code/imgs/03.png)


修复完成后尝试使用手机扫码，可以成功识别出二维码内容：

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Programming/%5B09%5D%20%5B40P%5D%20Quick%20Response%20Code/imgs/04.png)

## 解题代码

此代码是用 python 3.5.2 写的，运行此代码的几个前提：

- 已安装 zxing 二维码识别库，安装命令 `pip install zxing`
- 已安装 JDK 1.7 ，这是 [zxing](https://github.com/zxing/zxing) 要用的，它本质就是一个 Java 项目

> 注：
　　Windows环境下，若安装了含 JDK 1.7 在内的多个 JDK 却依然报错：
　　`Error: Registry key 'Software\JavaSoft\Java Runtime Environment'\CurrentVersion'`
 　　`has value '1.8', but '1.7' is required.`
　　只需要把 `C:\Windows\System32` 和 `C:\Windows\SysWOW64` 目录下的所有 `java.exe`、 `javaw.exe`、 `javaws.exe` 删除即可。


```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import base64
import urllib.request, urllib.parse
import http.cookiejar
from io import BytesIO
from PIL import Image
from PIL import ImageDraw
import zxing
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CHARSET = 'utf-8'
ROOTME_URL = 'http://challenge01.root-me.org/programmation/ch7/'


def main() :
    """
    主函数

    Returns:
        None
    """

    print('Init cookies ...')
    init_cookies()

    print('Get QR-Code image datas ...')
    image_byte = download_image()

    print('Fix QR-Code image ...')
    qrcode_path = fix_image(image_byte)

    print('Recognize ...')
    key = recognize(qrcode_path)
    print(' => %s' % key)

    print('Sumbit key ...')
    password = submit(key)
    print(' => %s' % password)


    # 显示图片（不是必须的，只是为了方便查看二维码）
    print('Show Image ...')
    image = Image.open(qrcode_path)
    image.show()
    os.remove(qrcode_path)



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


def download_image() :
    """
    从挑战页面下载二维码图片

    Returns:
        二维码图片数据（bytes）
    """

    lines = urllib.request.urlopen(ROOTME_URL).readlines()
    html = lines[0].decode(CHARSET)

    # 从页面代码中截取 Base64 图片数据, 格式形如： data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPoA.....
    pattern = re.compile(r'base64,([^"]+)')
    mth = pattern.search(html)
    image_data = mth.group(1)
    image_byte = base64.b64decode(image_data)    # Base64 解码成 bytes
    return image_byte


def fix_image(image_byte) :
    """
    图片修复：补全二维码三个角落的 “回” 形图案

    Args:
        image_byte: 二维码图片数据（bytes）

    Returns:
        修复后的二维码图片临时存储路径
    """

    image = Image.open(BytesIO(image_byte))
    draw = ImageDraw.Draw(image)

    w = 9       # 二维码中的每个大像素点是由 9x9 个像素构成
    w2 = w * 2
    w5 = w * 5
    w6 = w * 6
    w7 = w * 7
    for x, y in [(18, 18), (18, 216), (216, 18)] :
        draw.rectangle([(x, y), (x + w7, y + w7)], fill = BLACK)           # 绘制 “回” 外圈
        draw.rectangle([(x + w, y + w), (x + w6, y + w6)], fill = WHITE)   # 绘制 “回” 镂空区域
        draw.rectangle([(x + w2, y + w2), (x + w5, y + w5)], fill = BLACK) # 绘制 “回” 内核

    TMP_QRCODE_PATH = './tmp_qrcode.png'
    image.save(TMP_QRCODE_PATH, format='PNG')
    return TMP_QRCODE_PATH


def recognize(qrcode_path) :
    """
    使用 zxing 识别二维码内容

    Args:
        qrcode_path: 二维码图片存储路径

    Returns:
        从二维码图片内容中提取的 key 值
    """

    reader = zxing.BarCodeReader()
    qrcode = reader.decode(qrcode_path)
    content = qrcode.parsed
    key = re.sub(re.compile(r'^The key is '), '', content)
    return key


def submit(key) :
    """
    提交二维码内容中的 key 值

    Args:
        key: 二维码内容中的 key 值

    Returns:
        若没超时且 key 值正确，则返回 CTF 密码
    """

    params = urllib.parse.urlencode({ 'metu' : key })
    post_data = bytes(params, CHARSET)
    lines = urllib.request.urlopen(ROOTME_URL, post_data).readlines()
    html = lines[0].decode(CHARSET)

    mth = re.match(r'.*?Congratz, le flag est (\w+).*$', html)
    password = ('Success: %s' % mth.group(1)) if mth else 'Error or Timeout'
    return password



if __name__ == '__main__' :
    main()
```


------------



代码的调用结果如下，页面提示 `Congratz` 说明完成挑战：

```python
# captcha_me_if_you_can.py
Init cookies ...
Get QR-Code image datas ...
Fix QR-Code image ...
Recognize ...
 => /qrcod_7ueQF0
Sumbit key ...
 => Success: POHeyZ6pMvgn
Show image ...

Process finished with exit code 0
```

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2006~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
