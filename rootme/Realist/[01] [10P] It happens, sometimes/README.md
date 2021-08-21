## [[Root-Me](https://www.root-me.org/)] [[Realist](https://www.root-me.org/en/Challenges/Realist/)] [[It happens, sometimes](https://www.root-me.org/en/Challenges/Realist/It-happens-sometimes-93)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/realist/it-happens-sometimes/)]

------

我只想说出题人真的很无厘头，如果没有报复社会的心态，我想真的很难 Get 到这题的 Point 。

开启挑战后只有一篇公告（我后来才知道这篇公告是有其用意的），大意是说这个团队本来是打算做一个图片分类网站的，但是**被黑客删库跑路**了只能关停站点。

观察了源码和站内超链，并没有特别的地方。打开浏览器开发者工具，切到 Sources，发现有一个 images 文件夹，而且可以在页面查看文件夹的内容。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Realist/%5B01%5D%20%5B10P%5D%20It%20happens%2C%20sometimes/imgs/01.png)

文件夹里面只有 5 张图片和一个 Windows 的缩略图库 `Thumbs.db`，初步怀疑 `Thumbs.db` 应该有关键性的信息（因为其他图片不是都被黑客删了吗）。

网上搜索了一个 **ThumbsDBViewer** 工具，打开 `Thumbs.db`，可以发现里面有 22 张图片，逐一恢复后，基本都看不到什么特别，唯独 `41.jpg` 的信息有点可疑，但是像素太低根本看不到。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Realist/%5B01%5D%20%5B10P%5D%20It%20happens%2C%20sometimes/imgs/02.png)

到这里我就卡壳了，，，想了很久都没发现切入点。后来想到会不会有管理后台，于是尝试在 URL 末尾加了 `admin`，竟然蒙对了 ？？？ 真的弹出了一个输入管理员账密的提示框。

但是由于没有找到密码提示，于是尝试使用 Burp Suite 对 `admin` 页面进行常见密码爆破，无果。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Realist/%5B01%5D%20%5B10P%5D%20It%20happens%2C%20sometimes/imgs/03.png)

因为再也找不到切入点，确实把我惹烦了，我就想“你们不是被删库了吗，我就帮你们再删一次！”，也只是为了发泄，我就把 `admin` 页面请求动词从原本的 `GET` 改成了 `DELETE`，结果竟然返回了密码！！！ 卧槽？？？站长是自虐吧？？？这么喜欢别人删库跑路？？

不管过程如何，总算是完成挑战，而这题的题型很显然是 `HTTP Verb Tampering （HTTP动词篡改）`。我想如果一开始就有这个提示，所有东西都会变得简单。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Realist/%5B01%5D%20%5B10P%5D%20It%20happens%2C%20sometimes/imgs/04.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
