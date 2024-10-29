import socket
import threading
import time
import pickle
from ThreeBody_main import All

from ThreeBody_algorithm import star
import numpy as np
import sys
from ThreeBody_server import Server

sending_count = 0
start_time = time.time()

def main():
    # 初始条件
    start_time = time.time()
    star_1=star(300, 0.0, 0, 1, 10000)
    star_2=star(-300, 0.0, 0, -1, 10000)

    #初始star数组和spaceship数组
    stars=[star_1, star_2]

    spaceships=[]

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