## [[Root-Me](https://www.root-me.org/)] [[Network](https://www.root-me.org/en/Challenges/Network/)] [[FTP - authentication](https://www.root-me.org/en/Challenges/Network/FTP-authentication)] [[解题报告](http://exp-blog.com/2019/01/02/pid-2695/)]

------

题目的大意就是说有一个文件通过FTP传输了，希望可以找到这个FTP的使用者的密码。

点击挑战按钮后，会下载一份名为 `ch1.pcap` 的文件，做过网络抓包的话应该一眼就能认出这个后缀了。

用 Wireshark 打开这个文件，全部扫了一下，明显发现只有一个数据包是走了 `FTP-DATA` 的数据传输协议，说明之前 FTP 传输的就是这个文件。

右击 `FTP-DATA` 的数据包 -> 追踪流 -> TCP流：对这个数据包进行 TCP追踪，尝试找到建立这个 FTP 会话的数据包。

![](http://exp-blog.com/wp-content/uploads/2018/12/101b85aa3755c67a13ab475165a0f8f3.png)

马上就找到了建立这个 FTP 会话时发送的账号和密码请求，竟然是明文传输。。。完成挑战

![](http://exp-blog.com/wp-content/uploads/2018/12/3db182e14de3105c48f9b3b79ad000a0.png)

------

## 版权声明

　[![Copyright (C) 2016-2019 By EXP](https://img.shields.io/badge/Copyright%20(C)-2006~2019%20By%20EXP-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
