import socket

def start_client():
    print('客户端启动')
    # 创建CP/IP套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 连接服务器
    server_address = ('183.173.15.82', 65437)  # 替换为服务器的实际IP地址
    client_socket.connect(server_address)
    print('已连接到', server_address)
    try:
        while True:
            # 从用户输入获取数据
            message = input("请输入要发送的消息: ")
            if message:
                print('发送:', message)
                client_socket.sendall(message.encode())
                
                # 接收响应
                data = client_socket.recv(1024)
                print('收到:', data.decode())
            else:
                break
    finally:
        # 关闭连接
        client_socket.close()

if __name__ == "__main__":
    start_client()