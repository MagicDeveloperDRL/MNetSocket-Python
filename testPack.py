'''''''''
@file: testPack.py
@author: MRL Liu
@time: 2021/4/1 16:42
@env: Python3
@desc: 本模块用来设计测试服务端处理分包和粘包的能力
@ref: https://blog.csdn.net/yannanxiu/article/details/52096465
@blog: https://blog.csdn.net/qq_41959920
'''''''''
import socket
import time
import struct
import json

host = "localhost"
port = 5006

ADDR = (host, port)

if __name__ == '__main__':
    client = socket.socket()
    client.connect(ADDR)

    # 正常数据包定义
    ver = 1
    body = json.dumps(dict(hello="world"))
    print(body)
    cmd = 1
    header = [body.__len__(),cmd,ver]
    headPack = struct.pack("!3I", *header)
    sendData1 = headPack+body.encode()

    # 分包数据定义
    ver = 2
    body = json.dumps(dict(hello="world2"))
    print(body)
    cmd = 1
    header = [body.__len__(),cmd,ver]
    headPack = struct.pack("!3I", *header)
    sendData2_1 = headPack+body[:2].encode()
    sendData2_2 = body[2:].encode()

    # 粘包数据定义
    ver = 3
    body1 = json.dumps(dict(hello="world3"))
    print(body1)
    cmd = 1
    header = [body.__len__(),cmd,ver]
    headPack1 = struct.pack("!3I", *header)

    ver = 4
    body2 = json.dumps(dict(hello="world4"))
    print(body2)
    cmd = 1
    header = [body.__len__(),cmd,ver]
    headPack2 = struct.pack("!3I", *header)

    sendData3 = headPack1+body1.encode()+headPack2+body2.encode()

    # 正常数据包
    client.send(sendData1)
    time.sleep(3)

    # 分包测试
    client.send(sendData2_1)
    time.sleep(0.2)
    client.send(sendData2_2)
    time.sleep(3)

    # 粘包测试
    client.send(sendData3)
    time.sleep(3)
    client.close()


