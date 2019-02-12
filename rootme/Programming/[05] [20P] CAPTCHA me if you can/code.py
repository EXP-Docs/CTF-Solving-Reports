#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import re
import base64
import urllib.request, urllib.parse
import http.cookiejar
from io import BytesIO
from PIL import Image
from aip import AipOcr

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CHARSET = 'utf-8'
ROOTME_URL = 'http://challenge01.root-me.org/programmation/ch8/'

# 百度云在线 OCR 的 API 参数
# 去这里注册并创建一个文字识别应用即可获得：https://console.bce.baidu.com/ai/#/ai/ocr/overview/index
# 每天可以免费调用 500 次（超过 500 次则无法调用）
APP_ID = '15536930'
API_KEY = '1afN81Kiwy5bGIfy3jGBGIDU'
SECRET_KEY = 'w6OXaech6MN4Vs07X96NqqvKal0DGGPa'


def main() :
    """
    主函数

    Returns:
        None
    """

    print('Init cookies ...')
    init_cookies()

    bgn_time = get_system_millis()

    print('Get image datas ...')
    image_byte = download_image()

    print('Denoising ...')
    image_byte = denoising(image_byte)

    print('Recognize ...')
    captcha = recognize(image_byte)
    print(' => %s' % captcha)

    print('Sumbit captcha ...')
    password = submit(captcha)
    print(' => %s' % password)

    end_time = get_system_millis()
    print('Used time: %i ms' % (end_time - bgn_time))

    # 显示图片（不是必须的，只是为了方便对照验证码是否正确）
    print('Show Image ...')
    image = Image.open(BytesIO(image_byte))
    image.show()


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
    从挑战页面下载验证码图片

    Returns:
        图片数据（bytes）
    """

    lines = urllib.request.urlopen(ROOTME_URL).readlines()
    html = lines[0].decode(CHARSET)

    # 从页面代码中截取 Base64 图片数据, 格式形如： data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPoA.....
    pattern = re.compile(r'base64,([^"]+)')
    mth = pattern.search(html)
    image_data = mth.group(1)
    image_byte = base64.b64decode(image_data)    # Base64 解码成 bytes
    return image_byte


def denoising(image_byte) :
    """
    图片去噪（图片大小固定为 250x50，格式为 PNG）

    Args:
        image_byte: 图片数据（bytes）

    Returns:
        去噪后的图片数据（bytes）
    """

    image = Image.open(BytesIO(image_byte))
    pixel = image.load()

    # 噪点颜色为黑色，背景色为白色，因此只需要把黑色变成白色则完成去噪
    # 注：
    #   利用黑色去噪不是完美的，因为噪点的邻域像素区可能不是 100% 为纯黑色，可能导致残留。
    #   但观察发现残留噪点不多，所以可以忽略不计（更好的方式是设定一个灰度阀值去噪）。
    for x in range(250) :
        for y in range(50) :
            if pixel[x, y] == BLACK :
                pixel[x, y] = WHITE

    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return buffer.getvalue()


def recognize(image_byte) :
    """
    使用百度的在线 OCR API 进行图像识别

    Args:
        image_byte: 图片数据（bytes）

    Returns:
        识别的验证码
    """

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY) # 百度在线 OCR API，每天可以免费使用 500 次
    json = client.basicAccurate(image_byte)      # 格式形如： {'log_id': 311854091255477480, 'words_result': [{'words': "hSzjUDCQxqtz"}], 'words_result_num': 1}
    captcha = json['words_result'][0]['words']   # 提取识别出来的验证码

    # 修正验证码：
    #   虽然验证码中只会有 A-Z a-z 0-9 ，但是因为图片中可能存在残留噪点，
    #   这些残留噪点有几率会被识别成其他标点符号，需要去掉
    return re.sub(re.compile(r'[^A-Za-z0-9]'), '', captcha)


def submit(captcha) :
    """
    提交验证码

    Args:
        captcha: 验证码

    Returns:
        若没超时且验证码正确，则返回 CTF 密码
    """

    params = urllib.parse.urlencode({ 'cametu' : captcha })
    post_data = bytes(params, CHARSET)
    lines = urllib.request.urlopen(ROOTME_URL, post_data).readlines()
    html = lines[0].decode(CHARSET)

    mth = re.match(r'.*?Congratz, le flag est (\w+).*$', html)
    password = ('Success: %s' % mth.group(1)) if mth else 'Error or Timeout'
    return password


def get_system_millis() :
    """
    获取当前系统时间（用于计时）

    Returns:
        毫秒值
    """
    return int(round(time.time() * 1000))



if __name__ == '__main__' :
    main()
