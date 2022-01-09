'''
训练：仿照多进程并发模型，完成多线程网络并发模型实现相同功能
要求：使用面向对象的思想，类封装完成
'''
from threading import Thread
from socket import *

# 网络地址
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)

#创建线程做事情
class Handle(Thread):
    def __init__(self,conn,addr):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr

    # 实际干事情
    def run(self):
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            print(data.decode())
            self.conn.send(b'OK')
        self.conn.close()

#处理网络连接
class TCPServer:
    def __init__(self,host='',port=0):
        self.host = host
        self.port = port
        self.address = (host,port)
        self.sock = self._create_socket()

    def _create_socket(self):
        sock = socket()
        sock.bind(self.address)
        return sock

    # 处理客户端连接
    def _connet(self):
        conn, addr = self.sock.accept()
        print('Connect from', addr)
        # 创建一个线程为客户端服务
        t = Handle(conn,addr)
        t.start()



    def server_forever(self):
        self.sock.listen(5)
        print("Listen the port %d"%self.port)
        # 循环处理客户端连接
        while True:
            try:
                self._connet()
            except:
                self.sock.close()
                break
        print('服务结束')

if __name__ == '__main__':
    server = TCPServer(host='0.0.0.0',port=8888)
    server.server_forever() #启动服务