## [[Root-Me](https://www.root-me.org/)] [[Programming](https://www.root-me.org/en/Challenges/Programming/)] [[The Roman’s wheel](https://www.root-me.org/en/Challenges/Programming/The-Roman-s-wheel-151)] [[解题报告](https://exp-blog.com/safe/ctf/rootme/programming/the-roman-s-wheel/]

------

水题三连，与 [Go back to college](https://www.root-me.org/en/Challenges/Programming/Go-back-to-college-147)  、[Encoded string](https://www.root-me.org/en/Challenges/Programming/Encoded-string) 一模一样的解题方法，只是跟 robot 的交互消息改变了而已。

可以去参考 [Encoded string](https://www.root-me.org/en/Challenges/Programming/Encoded-string) 的[解题报告](http://exp-blog.com/2019/02/08/pid-3199/)，这两题的代码基本一模一样。

这题不再是 Base64 解码，题目已经明确告知是 **ROT13 解码**。

------------

ROT13 是凯撒加密算法的一个特例，该算法特点如下：

- 对于任意字符串，必定有 `string = ROT13(ROT13(string))`
- 只有 `A-Z`、`a-z` 英文字母需要做位移映射，其他字母保持原样
- 位移映射步长固定为 13 ，且若位移映射后超过字母范围，则绕回字母表开头进行映射
- 由前面性质可知，ROT13 的映射表是固定的：
　　键：`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`
　　值：`NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm`

------------


解题代码贴在下面（python 版本为 3.5.2）：

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import socket
CHARSET = 'utf-8'



def rot13(string) :
    """
    对给定字符串进行 ROT13 转码。
    注：
     (1) string = rot13(rot13(string))
     (2) 对于非 A-Z 和 a-z 范围内的字符，保持原样不转码

    Args:
        string: 原字符串

    Returns:
        转码后的字符串
    """

    text = ''
    for c in string :
        n = ord(c)
        ch = c
        if n >= ord('a') and n <= ord('m') :
            ch = chr(n + 13)

        elif n >= ord('A') and n <= ord('M') :
            ch = chr(n + 13)

        elif n >= ord('n') and n <= ord('z') :
            ch = chr(n - 13)

        elif n >= ord('N') and n <= ord('Z') :
            ch = chr(n - 13)

        text = '%s%s' % (text, ch)

    return text


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
                send_msg(irc_sock, bot_name, '!ep3')

            # :Candy!Candy@root-me.org PRIVMSG EXP :lLv0fyWosSgG3muQj3
            elif line.startswith(':%s' % bot_name) :
                mth = re.match(r':.+?:(\S+)$', line)
                if mth :
                    cipher = mth.group(1)
                    plain = rot13(cipher)
                    send_msg(irc_sock, bot_name, '!ep3 -rep %s' % plain)

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

运行代码后，结果如下：

```python
# the_romans_wheel.py
  =>  NICK EXP
  =>  USER EXP EXP EXP :http://exp-blog.com
  =>  JOIN #root-me_challenge
:irc.hackerzvoice.net NOTICE Auth :*** Looking up your hostname...
:irc.hackerzvoice.net 451 JOIN :You have not registered
:irc.hackerzvoice.net NOTICE Auth :*** Could not resolve your hostname: Domain name not found; using your IP address (223.74.73.34) instead.
:irc.hackerzvoice.net NOTICE Auth :Welcome to HackerzVoice!
:irc.hackerzvoice.net 001 EXP :Welcome to the HackerzVoice IRC Network EXP!EXP@223.74.73.34
:irc.hackerzvoice.net 002 EXP :Your host is irc.hackerzvoice.net, running version InspIRCd-2.0
:irc.hackerzvoice.net 003 EXP :This server was created 19:52:09 Aug 12 2013
:irc.hackerzvoice.net 004 EXP irc.hackerzvoice.net InspIRCd-2.0 BHIRSWcghiorswx FLMNPRSYabcefhijklmnopqrstvz FLYabefhjkloqv
:irc.hackerzvoice.net 005 EXP AWAYLEN=200 CALLERID=g CASEMAPPING=rfc1459 CHANMODES=be,k,FLfjl,MNPRScimnprstz CHANNELLEN=64 CHANTYPES=# CHARSET=ascii ELIST=MU EXCEPTS=e EXTBAN=,NRSUcjmz FNC KICKLEN=255 MAP :are supported by this server
:irc.hackerzvoice.net 005 EXP MAXBANS=60 MAXCHANNELS=20 MAXPARA=32 MAXTARGETS=20 MODES=20 NETWORK=HackerzVoice NICKLEN=31 OVERRIDE PREFIX=(Yqaohv)!~&@%+ SECURELIST SSL=0.0.0.0:6697 STARTTLS STATUSMSG=!~&@%+ :are supported by this server
:irc.hackerzvoice.net 005 EXP TOPICLEN=307 USERIP VBANLIST WALLCHOPS WALLVOICES :are supported by this server
:irc.hackerzvoice.net 042 EXP 959AAVAPE :your unique ID
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
:irc.hackerzvoice.net 251 EXP :There are 239 users and 83 invisible on 2 servers
:irc.hackerzvoice.net 252 EXP 2 :operator(s) online
:irc.hackerzvoice.net 254 EXP 106 :channels formed
:irc.hackerzvoice.net 255 EXP :I have 302 clients and 1 servers
:irc.hackerzvoice.net 265 EXP :Current Local Users: 302  Max: 355
:irc.hackerzvoice.net 266 EXP :Current Global Users: 322  Max: 375
:irc.hackerzvoice.net 396 EXP hzv-9ks.o51.eaqa1b.IP :is now your displayed host
:EXP!EXP@hzv-9ks.o51.eaqa1b.IP MODE EXP +x
  =>  PRIVMSG Candy :!ep3
:Candy!Candy@root-me.org PRIVMSG EXP :lLv0fyWosSgG3muQj3
  =>  PRIVMSG Candy :!ep3 -rep yYi0slJbfFtT3zhDw3
:Candy!Candy@root-me.org PRIVMSG EXP :You dit it! You can validate the challenge with the password 3bienBr4v0Continuepe7i7PONEY
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
