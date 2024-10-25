import socket
import time
import threading

def start_server():
    # 创建TCP/IP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 绑定套接字到所有可用的网络接口和端口
    server_address = ('0.0.0.0', 65437)
    server_socket.bind(server_address)
    
    # 监听传入的连接
    server_socket.listen(1)
    print('等待连接...')
    
    while True:
        # 接受连接
        connection, client_address = server_socket.accept()
        try:
            print('连接自', client_address)
            
            # 启动一个线程定期发送数据
            def send_zeros():
                while True:
                    connection.sendall(b'0')
                    time.sleep(1)

            threading.Thread(target=send_zeros, daemon=True).start()

            # 接收数据
            total_sum = 0
            while True:
                data = connection.recv(1024)
                if data:
                    a = int(data.decode())
                    print('收到:', a)
                    total_sum += a
                    print('发送:', total_sum)
                    connection.sendall(str(total_sum).encode())
                else:
                    break
        finally:
            # 关闭连接
            connection.close()

if __name__ == "__main__":
    start_server()