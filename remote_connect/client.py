import socket
import threading
import time
import keyboard

def receive_messages(client_socket):
    try:
        while True:
            # 接收服务器发送的数据
            data = client_socket.recv(1024)
            string=data.decode()
            if data:
                print('收到:', data.decode())
                print('收到:', string[2])
            else:
                break
            # 每秒钟打印一次
            time.sleep(1)
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
            if keyboard.is_pressed('a'):
                client_socket.sendall(b'a')
                time.sleep(0.1)
            if keyboard.is_pressed('s'):
                client_socket.sendall(b's')
                time.sleep(0.1)
            if keyboard.is_pressed('d'):
                client_socket.sendall(b'd')
                time.sleep(0.1)
            if keyboard.is_pressed('q'):
                client_socket.sendall(b'q')
                time.sleep(0.1)
            if keyboard.is_pressed('e'):
                client_socket.sendall(b'e')
                time.sleep(0.1)
            if keyboard.is_pressed('z'):
                client_socket.sendall(b'z')
                time.sleep(0.1)
            if keyboard.is_pressed('x'):
                client_socket.sendall(b'x')
                time.sleep(0.1)
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