import cv2
import numpy as np
# from ThreeBody_algorithm import Gravity
import time
import threading
from ThreeBody_movements import move
from ThreeBody_algorithm import star
import keyboard
from ThreeBody_operating import handle_key_0
from ThreeBody_operating import handle_key_1

from ThreeBody_delete import delete
from ThreeBody_destroy import destroy
from ThreeBody_image import DrawImage
frame=None

#绝对值函数，不知道哪里会用到，写着为好
def abs(x):
    if x<0:
        return -x
    else:
        return x

class All:
    def __init__(self,stars,spaceships,momentum_weapon,scale,bias_x,bias_y,last_creation_time_0,last_presstime_0,last_creation_time_1,last_presstime_1):
        self.stars=stars
        self.spaceships=spaceships
        self.momentum_weapon=momentum_weapon
        self.scale=scale
        self.bias_x=bias_x
        self.bias_y=bias_y
        self.last_creation_time_0=last_creation_time_0
        self.last_presstime_0=last_presstime_0
        self.last_creation_time_1=last_creation_time_1
        self.last_presstime_1=last_presstime_1

def run(all):
    # 调用各个文件中的总函数

    # 删除出界的星体和飞船
    delete(all.stars, all.spaceships, all.momentum_weapon)

    # 引力场移动星体和飞船
    move(all.stars, all.spaceships, all.momentum_weapon, 0.1)

    # 创建一个黑色背景的帧
    frame = np.zeros((1000, 1000, 3), dtype=np.uint8)

    # 画图
    frame = DrawImage(frame, all.stars, all.spaceships, all.momentum_weapon, all.scale, all.bias_x, all.bias_y)

    # 显示帧
    cv2.imshow('Moving Dot', frame)

    # 等待一段时间以控制帧率
    key = cv2.waitKey(int(10)) & 0xFF

    # 操作系统接收键盘输入
    if_continue, all.spaceships[0], all.momentum_weapon, all.scale, all.last_creation_time_0, all.last_presstime_0 = handle_key_0(
        key, all.spaceships[0], all.momentum_weapon, all.scale, all.last_creation_time_0, all.last_presstime_0)
    if_continue, all.spaceships[1], all.momentum_weapon, all.scale, all.last_creation_time_1, all.last_presstime_1 = handle_key_1(
        key, all.spaceships[1], all.momentum_weapon, all.scale, all.last_creation_time_1, all.last_presstime_1)

    all.spaceships, all.momentum_weapon = destroy(all.spaceships, all.momentum_weapon)

    # 如果按下q键，退出(operating模块会自当返回false)
    if not if_continue:
        return False,all
    return True,all    


def run0(all,key):
    # 调用各个文件中的总函数

    # 删除出界的星体和飞船
    delete(all.stars, all.spaceships, all.momentum_weapon)

    # 引力场移动星体和飞船
    move(all.stars, all.spaceships, all.momentum_weapon, 0.1)

    # # 创建一个黑色背景的帧
    # frame = np.zeros((1000, 1000, 3), dtype=np.uint8)

    # # 画图
    # frame = DrawImage(frame, all.stars, all.spaceships, all.momentum_weapon, all.scale, all.bias_x, all.bias_y)

    # # 显示帧
    # cv2.imshow('Moving Dot', frame)

    # # 等待一段时间以控制帧率
    # key = cv2.waitKey(int(10)) & 0xFF

    # 操作系统接收键盘输入
    if_continue, all.spaceships[0], all.momentum_weapon, all.scale, all.last_creation_time_0, all.last_presstime_0 = handle_key_0(
        key, all.spaceships[0], all.momentum_weapon, all.scale, all.last_creation_time_0, all.last_presstime_0)
    if_continue, all.spaceships[1], all.momentum_weapon, all.scale, all.last_creation_time_1, all.last_presstime_1 = handle_key_1(
        key, all.spaceships[1], all.momentum_weapon, all.scale, all.last_creation_time_1, all.last_presstime_1)

    all.spaceships, all.momentum_weapon = destroy(all.spaceships, all.momentum_weapon)

    # 如果按下q键，退出(operating模块会自当返回false)


    ###现在还没有加上q的功能###
    if not if_continue:
        return all
    return all    



def main():
    # 初始条件
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

    # 显示帧，这个视频一共有100000帧，总共为1000s
    for i in range(100000):
        # 调用run函数
        if_continue,all=run(all)
        if(if_continue==False):
            break

def DrawImage0(all):
    frame=np.zeros((1000, 1000, 3), dtype=np.uint8)
    DrawImage(frame, all.stars, all.spaceships, all.momentum_weapon, all.scale, all.bias_x, all.bias_y)

#执行主函数
if __name__ == '__main__':
    main()
