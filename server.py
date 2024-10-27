import socket
import threading
import time
import pickle
from ThreeBody_main import All
from ThreeBody_main import run0
from ThreeBody_algorithm import star
import numpy as np
import sys

sending_count = 0
start_time = time.time()

class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Server:
    def __init__(self, all,host='0.0.0.0', port=65437):
        self.all = all
        self.all_lock = threading.Lock()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print('等待连接...')   
    

    def handle_client(self, connection, client_address, notify_event):
        print('连接自', client_address)
        try:
            while True:
                data = connection.recv(1024)
                
                if data:
                    print('收到:', data.decode())
                    b = data.decode()
                    print(b)
                    ord_b=int(b)
                    with self.all_lock:
                        ###处理信息###
                        self.all=run0(self.all,ord_b)

                else:
                    print('客户端关闭连接')
                    break
        finally:
            connection.close()

    def send_periodic_message(self, connection, stop_event, notify_event):
        sending_count = 0
        while not stop_event.is_set():
            try:
                ###每次发送消息时都会对all进行处理，并且控制帧率###
                notify_event.wait(timeout=0.02)  
                notify_event.clear()  # 清除事件
                with self.all_lock:
                    ###每两帧发送一次###
                    for i in range(2):
                        self.all=run0(self.all, ord('0'))

                    serialized_all = pickle.dumps(self.all)
                    length = len(serialized_all)
                    ###发送消息###
                    connection.sendall(length.to_bytes(4, byteorder='big'))  # 发送数据长度
                    connection.sendall(serialized_all)  # 发送序列化对象
                    sending_count += 1

                    ###测试时间用，如果这里的输出比client中的输出快，则说明网络速度不够###
                    if sending_count==1:
                        global start_time
                        start_time = time.time()
                    if sending_count % 10==0:
                        end_time = time.time()
                        print(f"总时间: {end_time - start_time}")
                        print(f"发送次数: {sending_count}")
                    
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

def main():
    # 初始条件
    start_time = time.time()
    star_1=star(300, 0.0, 0, 1, 10000)
    star_2=star(-300, 0.0, 0, -1, 10000)
    spaceship0=star(50.0, 400.0, 0, 0,0)
    spaceship1=star(-50, 500.0, 0.0, 0.0, 0.0)
    #初始star数组和spaceship数组
    stars=[star_1, star_2]

    spaceships=[]
    spaceships.append(spaceship0)
    spaceships.append(spaceship1)

    #初始化动量武器数组，为空
    momentum_weapon=[]
    
    # 视频参数，定义舞台大小
    width, height = 1000, 1000
    # 创建一个黑色背景的帧
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    #初始化放大倍率和偏移量
    scale=1
    bias_x=0
    bias_y=0
    #初始化上一次按键时间（对于玩家0）
    last_creation_time_0=[time.time(),time.time(),time.time(),time.time(),time.time()]
    last_presstime_0=[time.time(),time.time(),time.time(),time.time(),time.time()]
    
    #初始化上一次按键时间（对于玩家1）
    last_creation_time_1=[time.time(),time.time(),time.time(),time.time(),time.time()]
    last_presstime_1=[time.time(),time.time(),time.time(),time.time(),time.time()]
    
    all=All(stars,spaceships,momentum_weapon,scale,bias_x,bias_y,
            last_creation_time_0,last_presstime_0,last_creation_time_1,last_presstime_1)
    server = Server(all)
    server.start()

if __name__ == "__main__":
    main()