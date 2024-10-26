import socket
import threading
import time
import pickle
import keyboard

class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def receive_messages(client_socket):
    try:
        while True:
            # 接收数据长度
            raw_length = client_socket.recv(4)
            if not raw_length:
                break
            length = int.from_bytes(raw_length, byteorder='big')
            
            # 接收实际数据
            data = b''
            while len(data) < length:
                more_data = client_socket.recv(length - len(data))
                if not more_data:
                    break
                data += more_data
            ###只要收到信息就打印出来###
            if data:
                try:
                    # 反序列化对象
                    received_object = pickle.loads(data)
                    if isinstance(received_object, Star):
                        print(f"Deserialized: x={received_object.x}, y={received_object.y}")
                    else:
                        print('收到:', data.decode())
                except (pickle.UnpicklingError, EOFError):
                    # 如果反序列化失败，打印原始数据
                    print('收到:', data.decode())
            else:
                break
            
    finally:
        # 关闭连接
        client_socket.close()

def send_messages(client_socket):
    try:
        while True:
            # 检测用户输入
            if keyboard.is_pressed('w'):
                client_socket.sendall(b'w')
                time.sleep(0.1)  # 防止发送过多的消息
    except Exception as e:
        print(f"发送消息时出错: {e}")

def start_client():
    print('客户端启动')
    # 创建TCP/IP套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 连接服务器
    server_address = ('183.172.255.12', 65437)  # 替换为服务器的实际IP地址
    client_socket.connect(server_address)
    print('已连接到', server_address)
    
    # 创建并启动接收消息的线程
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    
    # 创建并启动发送消息的线程
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

    # 等待线程结束
    receive_thread.join()
    send_thread.join()

if __name__ == "__main__":
    start_client()