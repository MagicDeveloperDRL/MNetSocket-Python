'''''''''
@file: ClientSocket.py
@author: MRL Liu
@time: 2021/3/31 21:48
@env: Python3
@desc: 提供基于Python程序的客户端通信功能
@ref:https://blog.csdn.net/yannanxiu/article/details/52096465
@blog: https://blog.csdn.net/qq_41959920
'''''''''
import json
import logging
import socket
from MsgProtol import MsgCmd,MsgProtol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("client")

class ClientSocket(object):
    def __init__(self, ip="127.0.0.1", port=5006):
        self.ip = ip  # ip地址
        self.port = port  # 端口号
        self._buffer_size = 12000  # 接收客户端消息的内存大小
        self.msg_protol =MsgProtol() # 网络通信协议

    def Connect(self):
        """初始化套接字"""
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建Socket对象
            self._socket.connect((self.ip,self.port)) # 连接服务器
            logger.info("客户端的IP地址是{}:{}".format(self.ip,self.port))
        except socket.error:
            self.close()
            raise socket.error("无法连接服务器，可能是服务器没有启动")

    def Send(self,cmd,data,recv):
        try:
            msg = self.msg_protol.pack(cmd,data,recv)
            self._socket.send(msg)  # 发送消息
            logger.info("发送1个数据包->cmd:" + MsgCmd(cmd).name+" body:"+str(data))
            # 是否接收回复
            if recv==1:
                self.Receive()
        except socket.error:
            raise

    def Receive(self):
        try:
            flag = True
            logger.info("开始接收消息...")
            while flag:
                msg = self._socket.recv(self._buffer_size)  # 接收消息
                flag = self.msg_protol.unpack(msg, self._handle_msg)  # 解封消息包
            logger.info("接收消息结束...")
        except socket.error as e:
            logging.debug("客户端接收消息出错")
            self.close()
            raise

    def _handle_msg(self,headPack,body):
        """分类处理接收到的消息字符串"""
        if  self._socket:
            # 数据处理
            cmd = MsgCmd(headPack[1]).name  # 获取Code的值
            is_recv = headPack[2]
            logging.info("收到1个数据包->bodySize:{}, cmd:{},recv:{}".format(headPack[0],cmd,is_recv))
            p = json.loads(body)  # 将字符串解码并且反序列化为json对象
            #print(body)
            # 检查消息类型
            if cmd == "EXIT": # 关闭消息
                self.close()
                return
            elif cmd == "INFORM": # 通知消息
                #msg = p["msg"]
                print(p)
            else:
                logging.error("\n未知的cmd:{0}".format(cmd))
            # 继续接收消息
            #self._recv_bytes()

    def close(self):
        try:
            if(self._socket!=None):
                self._socket.close()
                logger.info('套接字已经关闭')
        except socket.error:
            logging.debug("套接字关闭出错")
            raise

if __name__ == '__main__':
    client = ClientSocket()
    client.Connect()
    # 发送一个字典并且让服务端回复
    protol={}
    protol["type"] = MsgCmd.PARAM.name
    protol["apiNumber"]="大家伙"
    protol["AcademyName"] = "s"
    protol["logPath"] = "大家伙"
    protol["brainNames"] = "大家伙"
    protol["externalBrainNames"] = "s"
    # 发送消息
    client.Send(MsgCmd.PARAM.value,protol,1)