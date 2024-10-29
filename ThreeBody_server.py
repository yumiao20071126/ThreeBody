import socket
import threading
import time
import pickle
from ThreeBody_main import All, run, star
from ThreeBody_algorithm import star
from ThreeBody_operating import handle_key_0
import numpy as np
import sys

sending_count = 0
start_time = time.time()

class Server:
    def __init__(self, all, host='0.0.0.0', port=65437):
        self.all = all
        self.all_lock = threading.Lock()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = []  # 存储所有客户端连接
        self.client_spaceships = {}  # 存储每个客户端对应的飞船
        print('等待连接...')

    def run0(self, all, ord_b, spaceship):
        with self.all_lock:
            run(all, ord_b)

            if spaceship in self.all.spaceships:
                handle_key_0(ord_b, spaceship, self.all.momentum_weapon, self.all.scale, self.all.last_creation_time_0, self.all.last_presstime_0)


        return all

    def handle_client(self, connection, client_address, notify_event):
        print('连接自', client_address)
        try:
            while True:
                data = connection.recv(1024)
                
                if data:
                    print('收到:', data.decode())
                    b = data.decode()
                    print(b)
                    ord_b = int(b)
                    ###处理信息###
                    spaceship = self.client_spaceships[connection]
                    self.all = self.run0(self.all, ord_b, spaceship)

                else:
                    print('客户端关闭连接')
                    break
        finally:
            connection.close()
            self.clients.remove(connection)  # 移除断开的客户端
            del self.client_spaceships[connection]  # 移除对应的飞船

    def send_periodic_message(self, stop_event, notify_event):
        sending_count = 0
        while not stop_event.is_set():
            try:
                ###每次发送消息时都会对all进行处理，并且控制帧率###
                notify_event.wait(timeout=0.02)  
                notify_event.clear()  # 清除事件
                ###每两帧发送一次###
                for i in range(2):
                    self.all = self.run0(self.all, ord('0'), 0)

                if self.all is None:
                    print("Error: self.all is None")
                    continue

                serialized_all = pickle.dumps(self.all)
                length = len(serialized_all)
                ###广播消息给所有客户端###
                self.broadcast(length, serialized_all)
                sending_count += 1

                ###测试时间用，如果这里的输出比client中的输出快，则说明网络速度不够###
                if sending_count == 1:
                    global start_time
                    start_time = time.time()
                if sending_count % 50 == 0:
                    end_time = time.time()
                    print(f"总时间: {end_time - start_time}")
                    print(f"发送次数: {sending_count}")
                    
            except Exception as e:
                print(f"发送消息时出错: {e}")
                break

    def broadcast(self, length, serialized_all):
        for client in self.clients:
            try:
                client.sendall(length.to_bytes(4, byteorder='big'))  # 发送数据长度
                client.sendall(serialized_all)  # 发送序列化对象
            except Exception as e:
                print(f"发送消息给客户端时出错: {e}")
                self.clients.remove(client)  # 移除无法连接的客户端

    def add_spaceship(self, connection):
        with self.all_lock:
            new_spaceship = star(50.0, 200.0, 0.0, 0.0, 0.0)
            new_spaceship.name = f"spaceship_{len(self.clients)}"
            self.all.spaceships.append(new_spaceship)
            self.client_spaceships[connection] = new_spaceship

    def start(self):
        while True:
            connection, client_address = self.server_socket.accept()
            self.clients.append(connection)  # 添加新连接到客户端列表
            self.add_spaceship(connection)  # 增加一个飞船
            stop_event = threading.Event()
            notify_event = threading.Event()
            client_thread = threading.Thread(target=self.handle_client, args=(connection, client_address, notify_event))
            periodic_thread = threading.Thread(target=self.send_periodic_message, args=(stop_event, notify_event))
            client_thread.start()
            periodic_thread.start()

if __name__ == "__main__":
    all = All()  # 假设 All 类有一个无参数的构造函数
    server = Server(all)
    server.start()