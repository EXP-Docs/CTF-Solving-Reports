#!/usr/bin/python
# -*- coding: UTF-8 -*-

import base64
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
                send_msg(irc_sock, bot_name, '!ep2')

            # :Candy!Candy@root-me.org PRIVMSG EXP :WGdVSXdIaG5kOW9Vd3JQWkJzQXVsUnRqbWw=
            elif line.startswith(':%s' % bot_name) :
                mth = re.match(r':.+?:(\S+)$', line)
                if mth :
                    cipher = mth.group(1)
                    byte = base64.b64decode(cipher)         # base64 解码
                    plain = bytes.decode(byte, CHARSET)     # byte 转字符串
                    send_msg(irc_sock, bot_name, '!ep2 -rep %s' % plain)

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
