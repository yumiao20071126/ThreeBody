import socket

def start_client():
    print('客户端启动')
    # 创建TCP/IP套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 连接服务器
    server_address = ('127.0.0.1', 64438)  # 替换为服务器的实际IP地址
    client_socket.connect(server_address)
    print('已连接到', server_address)
    
    try:
        while True:
            # 从用户输入获取数据
            message = input("请输入要发送的消息 (输入 'exit' 退出): ")
            if message.lower() == 'exit':
                print('退出客户端')
                break

            if message:
                print('发送:', message)
                client_socket.sendall(message.encode())
                
                # 接收响应
                data = client_socket.recv(1024)
                if data:
                    print('收到:', data.decode())
                else:
                    print('服务器关闭连接')
                    break
        
    finally:
        # 关闭连接
        client_socket.close()

if __name__ == "__main__":
    start_client()