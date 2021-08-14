## [[Root-Me](https://www.root-me.org/)] [[Cryptanalysis](https://www.root-me.org/en/Challenges/Cryptanalysis/)] [[Hash - SHA-2](https://www.root-me.org/en/Challenges/Cryptanalysis/Hash-SHA-2)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/cryptanalysis/hash-sha@@@2/)]

------

水题，主要要有观察和分析能力，题目就是提示，SHA-2 解密。

需要知道 SHA-2 散列算法的特征， SHA-2 又分为两种算法，SHA-224 和 SHA-256。两者生成的密文都是由 `0-9a-fA-F` 组成的，其中 SHA-224 的密文长度固定是 56，SHA-256 的密文长度是 64 。

数了一下题目给出的密文串，是 65 个字符，而且不难发现其中多了一个范围外的字符 `k` 。

注意到题目描述说，这是截获下来的一段 Hash 码，而且在传输过程中出现错误，那么这个 `k` 很显然就是错误字符，将其去掉后密文串长度变成 64， 符合 SHA-256 的特征。

接下来就是对这个去掉 `k` 的密文串进行 SHA-256 解密了。但是很遗憾的是，我搜了很多在线的 SHA-256 解密工具，都没有收录这个密钥字条。不得已只能暴力碰撞破解，最终得到的明文串是 `4dM1n` （可能是彩蛋，不就是 admin 的变体么。。。）。

最后不要忘记，真正的答案还需要对 `4dM1n` 进行 SHA-1 加密，随便搜一个 [SHA-1 在线加密工具](http://www.ttmd5.com/hash.php?type=5)即可，完成挑战。

![](https://github.com/lyy289065406/CTF-Solving-Reports/blob/master/rootme/Cryptanalysis/%5B04%5D%20%5B5P%5D%20Hash%20-%20SHA-2/imgs/01.png)

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
