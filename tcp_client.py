"""
客户端
"""
import socket

# 创建套接字
socketfd = socket.socket()
# 连接服务期地址
socketfd.connect(("127.0.0.1", 8888))
# 收发信息
while True:
    data = input(">>>")
    if not data:
        break
    socketfd.send(data.encode())
# 关闭
socketfd.close()