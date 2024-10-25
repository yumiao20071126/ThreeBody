import socket
import threading
import time

# 全局变量 a 和锁
a = 0
a_lock = threading.Lock()

def add(a, b):
    if b == 'w':
        a += 100
    a += 1
    return a

def handle_client(connection, client_address, notify_event):
    global a
    print('连接自', client_address)
    try:
        while True:
            data = connection.recv(1024)
            if data:
                print('收到:', data.decode())
                b = data.decode()
                with a_lock:

                    ###处理信息###
                    a = add(a, b)
                    print(a)
                response = data.decode() + " (服务器已收到)"


                ###发送信息###
                connection.sendall(str(a).encode())
                
                ###发送信息###
                connection.sendall(response.encode())

                # 唤醒发送线程
                notify_event.set()
            else:
                print('客户端关闭连接')
                break
    finally:
        connection.close()

def send_periodic_message(connection, stop_event, notify_event):
    global a
    while not stop_event.is_set():
        try:
            notify_event.wait(timeout=1)  # 等待通知事件，超时1秒
            notify_event.clear()  # 清除事件
            with a_lock:

                ###对信息进行处理###
                a = add(a, '0')
                connection.sendall(str(a).encode())
        except Exception as e:
            print(f"发送消息时出错: {e}")
            break

def start_server():
    # 创建TCP/IP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 绑定套接字到所有可用的网络接口和端口
    server_address = ('0.0.0.0', 65437)
    server_socket.bind(server_address)
    
    # 监听传入的连接
    server_socket.listen(5)
    print('等待连接...')
    
    while True:
        connection, client_address = server_socket.accept()
        stop_event = threading.Event()
        notify_event = threading.Event()
        client_thread = threading.Thread(target=handle_client, args=(connection, client_address, notify_event))
        periodic_thread = threading.Thread(target=send_periodic_message, args=(connection, stop_event, notify_event))
        client_thread.start()
        periodic_thread.start()

if __name__ == "__main__":
    start_server()