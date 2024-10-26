import socket
import threading
import time
import pickle

class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Server:
    def __init__(self, host='0.0.0.0', port=65437):
        self.a = Star(10, 20)
        self.a_lock = threading.Lock()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print('等待连接...')
    ###这里是处理信息的函数###
    def add(self, a, b):
        if b == 'w':
            a.x += 100
        a.y += 1
        return a

    def handle_client(self, connection, client_address, notify_event):
        print('连接自', client_address)
        try:
            while True:
                data = connection.recv(1024)
                if data:
                    print('收到:', data.decode())
                    b = data.decode()
                    with self.a_lock:
                        ###处理信息###
                        self.a = self.add(self.a, b)
                        ax = self.a.x
                        ay = self.a.y
                        print(f"Deserialized: x={ax}, y={ay}")
                    response = data.decode() + " (服务器已收到)"
                    ###发送信息###
                    serialized_star = pickle.dumps(self.a)
                    length = len(serialized_star)
                    connection.sendall(length.to_bytes(4, byteorder='big'))  # 发送数据长度
                    connection.sendall(serialized_star)  # 发送序列化对象
                    notify_event.set()
                else:
                    print('客户端关闭连接')
                    break
        finally:
            connection.close()

    def send_periodic_message(self, connection, stop_event, notify_event):
        while not stop_event.is_set():
            try:
                notify_event.wait(timeout=1)  # 等待通知事件，超时1秒
                notify_event.clear()  # 清除事件
                with self.a_lock:
                    ###对信息进行处理###
                    self.a = self.add(self.a, '0')
                    serialized_star = pickle.dumps(self.a)
                    length = len(serialized_star)
                    connection.sendall(length.to_bytes(4, byteorder='big'))  # 发送数据长度
                    connection.sendall(serialized_star)  # 发送序列化对象
            except Exception as e:
                print(f"发送消息时出错: {e}")
                break

    def start(self):
        while True:
            connection, client_address = self.server_socket.accept()
            stop_event = threading.Event()
            notify_event = threading.Event()
            client_thread = threading.Thread(target=self.handle_client, args=(connection, client_address, notify_event))
            periodic_thread = threading.Thread(target=self.send_periodic_message, args=(connection, stop_event, notify_event))
            client_thread.start()
            periodic_thread.start()

if __name__ == "__main__":
    server = Server()
    server.start()