"""
epoll_sever.py 完成tcp并发服务
重点代码
思路分析：IO多路复用实现并发
        建立fileno-->io对象字典用于IO查找
"""

from socket import *
from select import *

# 创建监听套接字
s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 8888))
s.listen(5)

# 创建epoll对象
ep = epoll()
# 关注s
ep.register(s, EPOLLIN | EPOLLERR)
# 建立查找字典,通过一个IO的fileno找到IO对象
# 始终根register的IO保持一致
fmap = {s.fileno(): s}

# 循环监控IO发生
while True:
    events = ep.poll()
    # 循环遍历列表，查看哪个IO发生，进行处理
    for fd, event in events:
        if fd == s.fileno():
            c, addr = fmap[fd].accept()
            print("Connect from", addr)
            # 关注客户端套接字
            ep.register(c, EPOLLIN | EPOLLERR)
            fmap[c.fileno()] = c  # 维护字典
        elif event & EPOLLIN:  # 判断是否为EPOLLIN就绪
            data = fmap[fd].recv(1024).decode()
            if not data:
                ep.unregister(fd)  # 取消关注
                fmap[fd].close()
                del fmap[fd]  # 从字典中删除
                continue
            print(data)
            fmap[fd].send(b"OK")