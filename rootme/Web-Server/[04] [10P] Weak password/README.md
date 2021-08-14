## [[Root-Me](https://www.root-me.org/)] [[Web-Server](https://www.root-me.org/en/Challenges/Web-Server/)] [[Weak password](https://www.root-me.org/en/Challenges/Web-Server/Weak-password)] [[解题报告](http://exp-blog.com/2019/01/13/pid-2953/)]

------

看见题眼是弱密码，我第一反应就是用 `hydra` 工具进行爆破。

打开挑战页面后，弹出一个提示框要求输入账密，我顺手输入了 `admin:admin`。

竟然通过了。。。。

一万匹草泥马从我心头奔腾而过。。。真特喵不愧是弱密码。。。

重新检查了各个地方没找到其他提示，而且输入账密的请求并没有频率限制，可以肯定渗透套路就是直接爆破。

在爆破时需要注意账密不是明文提交的，用 Burp Suite 拦截请求时，可以发现提交的的账密被本地加密到了 `Authorization` 参数中，稍微分析后知道加密方式为 `Authorization="Basic " + to_base64(username:password)` 。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B04%5D%20%5B10P%5D%20Weak%20password/imgs/01.png)
![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Web-Server/%5B04%5D%20%5B10P%5D%20Weak%20password/imgs/02.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
