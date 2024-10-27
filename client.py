import socket
import threading
import time
import pickle
import keyboard
import numpy as np
from ThreeBody_main import All, run0
from ThreeBody_algorithm import star
from ThreeBody_main import DrawImage
import cv2
import sys

# 全局标志，用于终止主循环
terminate_flag = False

# 全局计数器，用于记录打印图片的次数
image_count = 0

def send_key_event(client_socket, event):
    global terminate_flag
    try:
        ####如果按下的是q，则终止程序####
        if event.name == 'q':
            terminate_flag = True

        ###发送的是键码，而不是字符###
        elif event.name in ['w', 'a', 's', 'd', 'z', 'x', 'e']:
            key_code = ord(event.name) if len(event.name) == 1 else event.name  # 获取按键的 ASCII 码或按键名称
            client_socket.sendall(str(key_code).encode())
    except Exception as e:
        print(f"发送消息时出错: {e}")

def send_messages(client_socket):
    try:
        # 监听所有按键事件
        keyboard.on_press(lambda event: send_key_event(client_socket, event))
        
        # 保持主线程运行
        ###防止重复发送###
        ###这里的时间可以调小一些，因为在operating中的函数会控制帧率###
        while not terminate_flag:
            time.sleep(1)
    except Exception as e:
        print(f"发送消息时出错: {e}")

def receive_messages(client_socket):
    global terminate_flag, image_count
    try:
        while not terminate_flag:
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
                    
                    # 创建一个黑色背景的帧
                    frame = np.zeros((1000, 1000, 3), dtype=np.uint8)

                    # 画图，函数已经的定义过了
                    ###其实可以直接写一个以结构体为自变量的函数###
                    frame = DrawImage(frame, received_object.stars, received_object.spaceships, 
                                      received_object.momentum_weapon, received_object.scale, 
                                      received_object.bias_x, received_object.bias_y)
                    
                    # 显示帧
                    cv2.imshow('Moving Dot', frame)
                    cv2.waitKey(1)

                    # 增加计数器
                    image_count += 1

                    ###测试时间用，如果这里的输出比client中的输出快，则说明网络速度不够###
                    if image_count % 10 == 0:
                        print(f"已打印图片次数: {image_count}")

                except (pickle.UnpicklingError, EOFError):
                    # 如果反序列化失败，打印原始数据
                    print('收到:', data.decode())
            else:
                break
    finally:
        # 关闭连接
        client_socket.close()

def start_client():
    global terminate_flag
    print('客户端启动')
    # 创建TCP/IP套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 连接服务器

    ###服务器IP地址###
    server_address = ('183.173.10.23', 65437)  # 替换为服务器的实际IP地址
    client_socket.connect(server_address)
    print('已连接到', server_address)
    
    # 创建并启动接收消息的线程
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    
    # 创建并启动发送消息的线程
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

    # 等待线程结束
    while not terminate_flag:
        time.sleep(1)

    # 终止程序
    receive_thread.join()
    send_thread.join()
    print("客户端已终止")

if __name__ == "__main__":
    start_client()