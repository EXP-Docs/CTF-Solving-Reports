## [[Root-Me](https://www.root-me.org/)] [[Programming](https://www.root-me.org/en/Challenges/Programming/)] [[CAPTCHA me if you can](https://www.root-me.org/en/Challenges/Programming/CAPTCHA-me-if-you-can)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/programming/captcha-me-if-you-can/)]

------

## 题目分析

恶心题。这题不难，但真的是麻烦，设计上是有瑕疵的。

题目要求很简单，3秒内破解并提交验证码。

在挑战页面只有一个验证码，每次刷新页面就会变化，观察发现验证码特征如下：

- 验证码字符范围为 `A-Z` 、`a-z` 、`0-9`
- 验证码字符没有任何变形（即扭曲、倾斜等），但有时会出现轻微旋转
- 图片存在噪点，但无干扰线
- 噪点总是黑色的，背景色总是白色的，验证码字符颜色会变化，但不会是黑白色
- 字符不等宽，字符间隔也不等宽，但是字符之间无粘连
- 字体是固定的，大小不固定
- 图片大小为 250x50 ， 格式为 PNG

## 解题思路

这道题是 2012 年出的，在当时要解决验证码识别问题，一般是走常规路子（原理性的东西，可以参考我的另一篇文章《[图像识别 - C++读取BMP位图入门](https://exp-blog.com/lang/cpp-tu-xiang-shi-bie/)》）：

- (1) 图像灰度化/二值化
- (2) 去噪（包括嘈点和干扰线）
- (3) 字符分割
- (4) 字符归一化（还原到扭曲、倾斜、旋转之前的形状，并统一缩放到某个固定大小）
- (5) 字符识别

实际上， (1) 到 (4) 都属于对图像的预处理工作，只有 (5) 才是真正开始做验证码的字符识别。


## 图像预处理

其实结合前面所分析的验证码特征，这题对图像的预处理是很好做的：

- (1) 去噪：由于噪点固定黑色且与字符不同色，可以通过把黑色变成白色背景色，简单去掉噪点，无需引入去噪算法
- (2) 图像二值化，使得字符前景色变成黑色，背景色则保持白色，便于后面的识别处理
- (3) 字符分割：虽然字符宽度和间隔宽度均是不等宽，但由于字符之间无粘连，可以用垂直扫描线从左到右扫描，只要扫描线上的像素点全为白色背景色，则为间隔区域，从而实现字符分割
- (4) 字符归一化：由于字符规正，直接缩放到同一大小即可，例如 32x32，再将其进行网格划分成 4×4 共16块（若有必要可继续划分）。通过可以计算每一块的特征值，最后就得到这个字符的 4×4 矩阵的网格特征值，这就是归一化（**其实就是卷积神经网络量化特征值的简化版**）。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Programming/%5B05%5D%20%5B20P%5D%20CAPTCHA%20me%20if%20you%20can/imgs/01.png)

## 字符识别

**传统的做法**：

预先准备标准的字符图像库（例如本例中只需准备 `A-Z` 、`a-z` 、`0-9` 共 62 个字符，字符采集可以直接人工从验证码里面挖），通过归一化提前计算图像库中每个字符的网格特征值作为参照特征值。

然后只需要把从验证码图像中提取的字符归一化所得到的网格特征值，**与这些参照特征值进行匹配，相似度最高的**，就认为识别成功。


------------

但现在已经是 2019 年了，在字符识别方面，我们有**更多的选择**：

- 专业的 **OCR** 工具：对于英文而且是规正字符的识别率很高，只需要装个驱动，其 SDK 提供了多种语言接口
- 近几年大火的**机器学习**：用 python 写一个专用的神经网络卷积算法，训练一个图像字符识别的模型库（可参考 TensorFlow 的 **MINIST** 是如何做的，示例代码可参考我的 [Github](https://github.com/lyy289065406/expcodes/tree/master/python/01-deep-learning)）
- **在线 OCR 平台**：如 [百度云](https://console.bce.baidu.com/ai/#/ai/ocr/overview/index)


------------

## 方案选择

站在出题人的角度，初衷应该是希望我们在本地用代码实现整个验证码识别算法的。

毕竟在 2012 年的时候，在线识别平台的技术还不成熟，延迟太高，要在 3 秒内完成整个过程基本是不可能的。

因此对出题人而言， 特征值匹配、OCR、机器学习 都是三个可接受的方案，而不会希望我们依赖在线识别平台。

我之前做爬虫的时候，这几套方案都做过，工作量排下来： **OCR < 特征值匹配 < 机器学习**。



------------

但无论哪个，在本地搞起来都是很麻烦。OCR 还好，装个驱动就可以了，不过需要找对所识别字符的字体库，不然识别率极低。其他两个因为训练素材基本都是临时找的，导致识别率普遍都不高（严格来说训练素材最好取自使用环境）。

所以我也就不费那个时间在本地搭环境了，**直接用百度的在线OCR API** ，不仅不需要对图片做太多预处理，识别率又高，而且在国内的响应时间已经能达到毫秒级（现在已经是 2019 年了，距离出题已经过去了 7 年，尤其是经过前两年人工智能、深度学习的洗礼，在图像识别这块已经做到相当成熟，其中国内又以百度的识别技术为最好，这也是我选百度的原因）。

> **注**：
　　我以前做爬虫，因为要模拟网页登陆，同样要识别验证码，所以搭过本地 OCR 环境，写过特征值匹配算法，写过神经网络卷积算法，封装过 TensorFlow，也实现过 MINIST，知道这些都是怎么一回事，所以在做这题的时候就不再重新搞了，毕竟不想为了一题 CTF 费事费力专门弄一套这么些东西，于是偷了个懒。
　　但是如果新同学没有弄过这些，建议还是弄一下，不要学我用在线 OCR ，毕竟亲自搞能学到不少东西，这也是我们做题的初衷。不要为了做题而做题，要从过程中学会自己未掌握的知识。


## 百度在线OCR

首先需要注册一个[百度云](https://cloud.baidu.com/)账号，然后在【[控制台](https://console.bce.baidu.com/ai/#/ai/ocr/overview/index)】选择【产品服务】->【文字识别】->【创建应用】

应用信息随便填即可，创建成功后会得到三个参数，后面调用 API 时要用到的： `APP_ID`、`API_KEY`、`SECRET_KEY`

这样就得到了 **每天免费 500 次** 的 OCR 识别权限，对于 CTF 是完全足够了。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Programming/%5B05%5D%20%5B20P%5D%20CAPTCHA%20me%20if%20you%20can/imgs/02.png)

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Programming/%5B05%5D%20%5B20P%5D%20CAPTCHA%20me%20if%20you%20can/imgs/03.png)


建议使用 python 进行开发，该 API 的 SDK 安装可以通过命令 `pip install baidu-aip` 简单实现。

详细的使用方式可参见百度官方文档：[http://ai.baidu.com/docs#/OCR-Python-SDK/top](http://ai.baidu.com/docs#/OCR-Python-SDK/top)

------------

## 解题代码

此代码是用 python 3.5.2 写的，运行此代码的几个前提：

- 已安装 PIL 库，安装命令 `pip install Pillow`
- 已安装百度在线 OCR SDK ， 安装命令 `pip install baidu-aip`
- 已注册百度云在线 OCR 应用并替换其中的三个 API 参数，详见 [上一节](http://exp-blog.com/2019/02/09/pid-3217/#OCR)
- 已在浏览器登陆了 rootme 并打开过此挑战页面


```python
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

```

这代码不是 100% 能 pass 的，尤其是在国内。

一方面是百度 API 识别验证码的准确率并不是 100% ，但据我观察大概是 90% 的样子（必须去噪，不去噪只有50%，另外旋转的问题不用处理，百度会自动处理）

不过所有识别方法都存在识别率的问题，所以多试几次就好，识别率并不影响我们解题。

------------


最麻烦的是，出题所要求的 3 秒内破解验证码，并没有把网络延迟考虑进去，而且国内跟 rootme 交互的延迟是很高的，普通网络要在 3 秒内完成两次跟 rootme 的交互（取图片+提交验证码）基本不可能实现（我测试裸连最短都要 4 秒）。

因此如果有云服务器的同学，建议把代码放到云服务器上跑；有办法科学上网的，就科学一下再跑。

我是把代码放到云服务器上跑的，整个过程最短是 1.2 秒，试了几次终于 pass 。

真搞不懂出题人的时间是怎么考虑的，测试的是网络延迟而不是算法识别时间，导致时间上只能碰运气，出题不严谨。

其实可以参考 POJ 的做法，在服务器沙盒运行代码验证时间复杂度。

------------


代码的调用结果如下，页面提示 `Congratz` 说明完成挑战：

```python
# captcha_me_if_you_can.py
Init cookies ...
Get image datas ...
Denoising ...
Recognize ...
 => hSzjUDCQxqtz
Sumbit captcha ...
 => Success: dtePZJgVAfaU
Used time: 1208 ms
Show image ...

Process finished with exit code 0
```

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
