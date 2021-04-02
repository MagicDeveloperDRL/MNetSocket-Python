'''''''''
@file: MsgProtol.py
@author: MRL Liu
@time: 2021/4/1 11:04
@env: Python3
@desc: 网络通信的消息协议
@ref: https://blog.csdn.net/yannanxiu/article/details/52096465
@blog: https://blog.csdn.net/qq_41959920
'''''''''
import json
import struct
from enum import Enum

class MsgCmd(Enum):
    INFORM = 1 # 通知，不需要回复
    REQUEST = 2 # 请求，需要回复
    PARAM =3 # 参数
    EXIT = 4 #退出

class MsgProtol(object):
    def __init__(self):
        self.dataBuffer = bytes() # 接收消息的缓存
        self.headerSize = 12 # 3*4，消息头的字节总数


    def pack(self,cmd,_body,_recv=1):
        body = json.dumps(_body) # 将消息正文转换成Json格式，并转换成字节编码
        header = [body.__len__(),cmd,_recv] # 将消息头按顺序组成一个列表
        headPack= struct.pack("3I", *header) #  使用struct打包消息头,得到字节编码
        sendData = headPack+body.encode("utf8")  # 将消息头字节和消息正文字节组合在一起
        return sendData

    def unpack(self,data,msgHandler):
        if data:
            self.dataBuffer += data
            while True:
                # 数据量不足消息头部时跳出函数继续接收数据
                if len(self.dataBuffer) < self.headerSize:
                    #print("数据包（%s Byte）小于消息头部长度，跳出小循环" % len(self.dataBuffer))
                    break
                # struct中:!代表Network order，3I代表3个unsigned int数据
                #msg_length = struct.unpack("I", bytearray(msg[:4]))[0]  # 获取信息长度
                headPack = struct.unpack('3I', bytearray(self.dataBuffer[:self.headerSize]))# 解码出消息头部
                # 获取消息正文长度
                bodySize = headPack[0]
                # 分包情况处理，跳出函数继续接收数据
                if len(self.dataBuffer) < self.headerSize + bodySize:
                    #print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" % (len(self.dataBuffer), self.headerSize + bodySize))
                    break
                # 读取消息正文的内容
                body = self.dataBuffer[self.headerSize:self.headerSize + bodySize]
                msgHandler(headPack,body.decode("utf8"))
                # 粘包情况的处理，获取下一个数据包部分
                self.dataBuffer = self.dataBuffer[self.headerSize + bodySize:]
            if len(self.dataBuffer)!=0:
                return True # 继续接收消息
            else:
                return False  # 不再接收消息
        else:
            return False # 不再接收消息


