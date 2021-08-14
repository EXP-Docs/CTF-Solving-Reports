## [[Root-Me](https://www.root-me.org/)] [[Programming](https://www.root-me.org/en/Challenges/Programming/)] [[Go back to college](https://www.root-me.org/en/Challenges/Programming/Go-back-to-college-147)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/programming/go-back-to-college/)]

------

水题，有点像读书时参加的 ACM 比赛，确实有点 Go back to college 的感觉。

题目意思大概就是有一个 IRC 聊天室频道，里面有一个 robot 名为 Candy 。

我们要连接到这个 IRC 频道，与 Candy 进行交互以开启挑战。

挑战过程和要求如下：

- 连接到 IRC 聊天服务器，并进入指定 robot Candy 所在的聊天频道
- 发送消息 ` !ep1` 给 Candy
- Candy 会以固定格式 `<number1> / <number2>` 回复两个数字，如： `429 / 5134`
- 我们需要在 **2秒内** 计算 `answer = sqrt(number1) * number2` ，且 `answer` 保留 **2位小数**
- 然后发送固定格式的消息 `!ep1 -rep <answer>` 给 Candy
- Candy 验证结果后，会回复我们想要的 flag 以完成挑战


------------

看了过程就知道这题是真的非常简单，<font color="red">关键是要弄懂 IRC 协议怎么连接、怎么交互</font>。

IRC 全称 Internet Relay Chat ，即互联网中继聊天，它是一种网络聊天协议。

IRC的工作原理非常简单，只要在自己的 PC 上运行客户端软件，然后通过因特网以 IRC 协议连接到一台 IRC 服务器上即可。它的特点是速度非常之快，聊天时几乎没有延迟的现象，并且仅仅占用很少的带宽资源。所有用户可以在一个被称为 Channel（频道） 的地方就某一话题进行交谈或密谈。每个 IRC 的使用者都有一个 Nickname（昵称）。

国内听过的人 IRC 的人不多，用过的人就更少了。但是国外应该是比较火的，其功能类似于 QQ，但由于聊天记录的私密性（连管理员都无法查看任意两个人之间私信的聊天记录），所以很多 Hacker 之间的交流都会使用它。

------------

从本质上看，其实这题下载任何一个现成的 IRC 客户端，使用人工交互方式就可以做，毕竟运算量很少。但是题目为了避免我们这样投机取巧，要求在 **2秒内** 计算结果并返回，这样就不能不依赖编程实现了。

在这里我选择了 python ，关于 python 如何连接到 IRC 的聊天频道，详细可以参考 [这篇文章](https://www.cnblogs.com/jinmu190/archive/2010/11/18/1880392.html) 。

我就不复述了，直接贴代码（python 版本为 3.5.2）：

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import socket
CHARSET = 'utf-8'



def send_cmd(irc_sock, cmd) :
    """
    发送命令到 IRC 服务器

    Args:
        irc_sock: 与 IRC 服务器的 socket 连接
        cmd: 待发送的命令（不需 \r\n 结束符，会自动补全）

    Returns:
        None
    """

    print('  =>  %s' % cmd)
    irc_sock.send(('%s\r\n' % cmd).encode(CHARSET))
    return


def send_msg(irc_sock, to, msg) :
    """
    发送 PRIVMSG 私信命令到 IRC 服务器

    Args:
        irc_sock: 与 IRC 服务器的 socket 连接
        to: 接收私信的对象
        msg: 待发送的私信内容

    Returns:
        None
    """

    cmd = 'PRIVMSG %s :%s' % (to, msg)
    send_cmd(irc_sock, cmd)
    return


def conn_irc(irc_host, irc_port, irc_chan, username, anywords) :
    """
    连接到 IRC 服务器的指定聊天频道

    Args:
        irc_host: IRC 服务器主机
        irc_port: IRC 服务端口
        irc_chan: IRC 聊天频道
        username: 在 IRC 聊天室标识自己身份的昵称（任意值均可，只要未被他人在 IRC 上使用即可）
        anywords: 首次加入 IRC 聊天室后用于打招呼的语句，任意即可

    Returns:
        irc_sock: 与 IRC 服务器的 socket 连接
    """

    irc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc_sock.connect((irc_host, irc_port))

    # NICK 和 USER 命令必须先发送，以声明自己身份
    # （注意同一个 IP 不能同时开两次以上的连接，否则只有第一次能够注册成功）
    send_cmd(irc_sock, 'NICK %s' % username)
    send_cmd(irc_sock, 'USER %s %s %s :%s' % (username, username, username, anywords))
    send_cmd(irc_sock, 'JOIN %s' % irc_chan)    # 加入频道
    return irc_sock



def interface(irc_sock, bot_name, username) :
    """
    在 IRC 聊天室与 robot 进行消息交互

    Args:
        irc_sock: 与 IRC 服务器的 socket 连接
        bot_name: 机器人的昵称
        username: 自己的昵称

    Returns:
        None
    """

    finish = False
    while finish == False :
        rsp_data = irc_sock.makefile(encoding=CHARSET)

        # 逐行解析响应数据
        for line in rsp_data:
            print(line, end='')

            if line.startswith('PING') :
                send_cmd(irc_sock, line.replace('PING', 'PONG'))

            # :EXP!EXP@hzv-tsd.o51.eaqa1b.IP MODE EXP +x
            elif line.startswith(':%s' % username) :
                send_msg(irc_sock, bot_name, '!ep1')

            # :Candy!Candy@root-me.org PRIVMSG EXP :645 / 8814
            elif line.startswith(':%s' % bot_name) :
                mth = re.match(r':.+?:(\d+) / (\d+)$', line)
                if mth :
                    n1 = int(mth.group(1))
                    n2 = int(mth.group(2))
                    rst = (n1 ** 0.5) * n2     # n1 的平方根乘以 n2
                    answer = round(rst, 2)     # 结果保留 2 位小数
                    send_msg(irc_sock, bot_name, '!ep1 -rep %s' % answer)

                else :
                    send_cmd(irc_sock, 'QUIT')  # 退出聊天频道
                    finish = True
                    break
    return


if __name__ == '__main__' :
    irc_host = 'irc.root-me.org'
    irc_port = 6667
    irc_chan = '#root-me_challenge'
    bot_name = 'Candy'
    username = 'EXP'
    anywords = 'http://exp-blog.com'

    # 连接到 ROOTME 的 IRC 聊天室并加入 CHALLENGE 聊天频道
    irc_sock = conn_irc(irc_host, irc_port, irc_chan, username, anywords)

    # 在聊天室与 robot 进行消息交互
    interface(irc_sock, bot_name, username)

    # 关闭 IRC 的 socket 连接
    irc_sock.shutdown(2)
    irc_sock.close()

```

其实代码很简单，rootme 已经给出了 IRC 服务器的 host 和 端口，直接使用 socket 连接即可。

关键是连接后要使用 IRC 的协议进行交互。

这里需要注意的有几点（详细可以参考代码）：

- 用到的 IRC 命令主要有：`NICK`、`USER`、`JOIN`、`PRIVMSG`
- 每个 IRC 命令都有固定的格式，多一个空格少一个空格都可能会造成交互异常
- 每条 IRC 命令必定以 `\r\n` 结尾
- 连接到 IRC 服务器后，`NICK` 和 `USER` 命令必须先于所有命令发送，以标称自己的身份
- 上述代码中涉及到的 IRC 命令格式和样例见下表：


| IRC 命令 | 格式 | 样例 | 作用 |
|:---:|:---:|:---:|:---:|
| `NICK` | `NICK [username]\r\n` | `NICK EXP\r\n` | 设置在聊天室的昵称，连接到 IRC 服务器后必须首先发送此命令 |
| `USER` | `USER [username] [username] [username] :[any_msg]\r\n` | `NICK EXP EXP EXP :Hi\r\n` | 我找不到关于这条命令的任何说明，但是它必须跟在 `NICK` 命令后 |
| `JOIN` | `JOIN [channel]\r\n` | `JOIN #root-me_challenge\r\n` | 加入某个聊天频道，<br/>频道名称必须以 # 开头 |
| `PRIVMSG` | `PRIVMSG [somebody] :[any_msg]\r\n` | `PRIVMSG Candy :Hello\r\n` | 给某人发送私信 |

------------

运行代码后，结果如下（注意，以 `  =>  ` 开头表示是代码发送的 IRC 命令，其他均是 IRC 服务器返回的内容）：

```python
# go_back_to_college.py
  =>  NICK EXP
  =>  USER EXP EXP EXP :http://exp-blog.com
  =>  JOIN #root-me_challenge
:irc.hackerzvoice.net NOTICE Auth :*** Looking up your hostname...
:irc.hackerzvoice.net 451 JOIN :You have not registered
:irc.hackerzvoice.net NOTICE Auth :*** Could not resolve your hostname: Domain name not found; using your IP address (223.74.73.30) instead.
:irc.hackerzvoice.net NOTICE Auth :Welcome to HackerzVoice!
:irc.hackerzvoice.net 001 EXP :Welcome to the HackerzVoice IRC Network EXP!EXP@223.74.73.30
:irc.hackerzvoice.net 002 EXP :Your host is irc.hackerzvoice.net, running version InspIRCd-2.0
:irc.hackerzvoice.net 003 EXP :This server was created 19:52:09 Aug 12 2013
:irc.hackerzvoice.net 004 EXP irc.hackerzvoice.net InspIRCd-2.0 BHIRSWcghiorswx FLMNPRSYabcefhijklmnopqrstvz FLYabefhjkloqv
:irc.hackerzvoice.net 005 EXP AWAYLEN=200 CALLERID=g CASEMAPPING=rfc1459 CHANMODES=be,k,FLfjl,MNPRScimnprstz CHANNELLEN=64 CHANTYPES=# CHARSET=ascii ELIST=MU EXCEPTS=e EXTBAN=,NRSUcjmz FNC KICKLEN=255 MAP :are supported by this server
:irc.hackerzvoice.net 005 EXP MAXBANS=60 MAXCHANNELS=20 MAXPARA=32 MAXTARGETS=20 MODES=20 NETWORK=HackerzVoice NICKLEN=31 OVERRIDE PREFIX=(Yqaohv)!~&@%+ SECURELIST SSL=0.0.0.0:6697 STARTTLS STATUSMSG=!~&@%+ :are supported by this server
:irc.hackerzvoice.net 005 EXP TOPICLEN=307 USERIP VBANLIST WALLCHOPS WALLVOICES :are supported by this server
:irc.hackerzvoice.net 042 EXP 959AAU9R1 :your unique ID
:irc.hackerzvoice.net 375 EXP :irc.hackerzvoice.net message of the day
:irc.hackerzvoice.net 372 EXP :-     ██████████     ╻ ╻┏━┓┏━╸╻┏ ┏━╸┏━┓╺━┓╻ ╻┏━┓╻┏━╸┏━╸
:irc.hackerzvoice.net 372 EXP :-   ████████    ██   ┣━┫┣━┫┃  ┣┻┓┣╸ ┣┳┛┏━┛┃┏┛┃ ┃┃┃  ┣╸ 
:irc.hackerzvoice.net 372 EXP :-   ██    ██    ██   ╹ ╹╹ ╹┗━╸╹ ╹┗━╸╹┗╸┗━╸┗┛ ┗━┛╹┗━╸┗━╸
:irc.hackerzvoice.net 372 EXP :-   ██████████████   
:irc.hackerzvoice.net 372 EXP :-     ██████████     IRC network at irc.hackerzvoice.net.
:irc.hackerzvoice.net 372 EXP :-     ██  ██  ██     HZV will never die.
:irc.hackerzvoice.net 372 EXP :- 
:irc.hackerzvoice.net 372 EXP :- 
:irc.hackerzvoice.net 372 EXP :- Bienvenue sur l'irc HackerzVoice !
:irc.hackerzvoice.net 372 EXP :- ==================================
:irc.hackerzvoice.net 372 EXP :- 
:irc.hackerzvoice.net 372 EXP :- - Besoin d'aide ? Rejoignez nous sur #help : /join #help
:irc.hackerzvoice.net 372 EXP :- 
:irc.hackerzvoice.net 372 EXP :- ----- Règles du serveur --------------------------------------
:irc.hackerzvoice.net 372 EXP :-  [+] No flooding
:irc.hackerzvoice.net 372 EXP :-  [+] No DoS bots
:irc.hackerzvoice.net 372 EXP :-  [+] No clones
:irc.hackerzvoice.net 372 EXP :-  [+] No spamming
:irc.hackerzvoice.net 372 EXP :-  [+] No takeovers
:irc.hackerzvoice.net 372 EXP :-  [+] No whiners
:irc.hackerzvoice.net 372 EXP :- --------------------------------------------------------------
:irc.hackerzvoice.net 372 EXP :- 
:irc.hackerzvoice.net 372 EXP :- Il est possible de se connecter à ce serveur :
:irc.hackerzvoice.net 372 EXP :- - irc.hackerzvoice.net:6667
:irc.hackerzvoice.net 372 EXP :- - irc.hackerzvoice.net:6697 (SSL)
:irc.hackerzvoice.net 372 EXP :- 
:irc.hackerzvoice.net 372 EXP :- ### Contact
:irc.hackerzvoice.net 372 EXP :- 
:irc.hackerzvoice.net 372 EXP :- Admin : Hackira (hackira@hzv.fr)
:irc.hackerzvoice.net 372 EXP :- 
:irc.hackerzvoice.net 372 EXP :- #### Sites web
:irc.hackerzvoice.net 372 EXP :- - https://www.hackerzvoice.net/
:irc.hackerzvoice.net 372 EXP :- - https://www.lehack.org/
:irc.hackerzvoice.net 372 EXP :- 
:irc.hackerzvoice.net 372 EXP :- #### Réseaux sociaux
:irc.hackerzvoice.net 372 EXP :- - Twitter : https://www.twitter.com/asso_hzv
:irc.hackerzvoice.net 376 EXP :End of message of the day.
:irc.hackerzvoice.net 251 EXP :There are 255 users and 86 invisible on 2 servers
:irc.hackerzvoice.net 252 EXP 2 :operator(s) online
:irc.hackerzvoice.net 254 EXP 107 :channels formed
:irc.hackerzvoice.net 255 EXP :I have 321 clients and 1 servers
:irc.hackerzvoice.net 265 EXP :Current Local Users: 321  Max: 355
:irc.hackerzvoice.net 266 EXP :Current Global Users: 341  Max: 375
:irc.hackerzvoice.net 396 EXP hzv-tsd.o51.eaqa1b.IP :is now your displayed host
:EXP!EXP@hzv-tsd.o51.eaqa1b.IP MODE EXP +x
  =>  PRIVMSG Candy :!ep1
:Candy!Candy@root-me.org PRIVMSG EXP :429 / 5134
  =>  PRIVMSG Candy :!ep1 -rep 106337.03
:Candy!Candy@root-me.org PRIVMSG EXP :You dit it! You can validate the challenge with the password jaimlefr0m4g
  =>  QUIT

Process finished with exit code 0
```

其实前面一大段 `:irc.hackerzvoice.net ******` 都是连接到 IRC 聊天室后自动返回的画屏信息，最后几行才是真正的交互内容。显然地，我计算出了结果并成功得到了密码。

> 注：若网络不好导致 2秒内 没有发送成功， IRC 会提示 `too late` ，多试几次就好

------

## 版权声明

　[![Copyright (C) EXP,2016](https://img.shields.io/badge/Copyright%20(C)-EXP%202016-blue.svg)](http://exp-blog.com)　[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  

- Site: [http://exp-blog.com](http://exp-blog.com) 
- Mail: <a href="mailto:289065406@qq.com?subject=[EXP's Github]%20Your%20Question%20（请写下您的疑问）&amp;body=What%20can%20I%20help%20you?%20（需要我提供什么帮助吗？）">289065406@qq.com</a>


------
