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
