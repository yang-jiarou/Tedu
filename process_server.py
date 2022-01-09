'''
多进程并发模型
'''
from multiprocessing import Process
from socket import *

#网络地址
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)

#具体处理客户端请求
def handle(conn,addr):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data.decode())
        conn.send(b'OK')
    conn.close()

#处理客户端连接
def connet(sock):
    conn, addr = socket.accept()
    print('Connect from', addr)
    # 创建一个进程为客户端服务
    p = Process(target=handle, args=(conn, addr),daemon=True)
    p.start()

#网络准备工作
def main():
    # 创建套接字
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)
    print("Listen the port %d"%PORT)

    #循环处理客户端连接
    while True:
        try:
            connet(sock)
        except:
            sock.close()
            break
    print('服务结束')

if __name__ == '__main__':
    main()