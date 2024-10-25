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
    
    # 显示帧，这个视频一共有100000帧，总共为1000s
    for i in range(100000):

        #调用各个文件中的总函数

        #删除出界的星体和飞船
        delete(stars,spaceships, momentum_weapon)

        #引力场移动星体和飞船
        move(stars, spaceships, momentum_weapon, 0.1)

        # 创建一个黑色背景的帧
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        #画图
        frame=DrawImage(frame,stars,spaceships, momentum_weapon,scale,bias_x,bias_y)

        # 显示帧
        cv2.imshow('Moving Dot', frame)

        # 等待一段时间以控制帧率
        key = cv2.waitKey(int(10)) & 0xFF

        #操作系统接收键盘输入
        if_continue, spaceship0, momentum_weapon, scale, last_creation_time_0, last_presstime_0=handle_key_0(key, spaceship0, momentum_weapon, scale,last_creation_time_0, last_presstime_0)
        if_continue, spaceship1, momentum_weapon, scale, last_creation_time_1, last_presstime_1=handle_key_1(key, spaceship1, momentum_weapon, scale,last_creation_time_1, last_presstime_1)

        spaceships, momentum_weapon=destroy(spaceships, momentum_weapon)

        #如果按下q键，退出(operating模块会自当返回false)
        if(if_continue==False):
            break
        
#执行主函数
if __name__ == '__main__':
    main()
