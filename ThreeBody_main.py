import cv2
import numpy as np

from ThreeBody_movements import move
from ThreeBody_algorithm import star
import keyboard
from ThreeBody_operating import handle_key_0

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

def run(all,key_input):
    # 调用各个文件中的总函数
    key=key_input
    # 删除出界的星体和飞船
    delete(all.stars, all.spaceships, all.momentum_weapon)

    # 引力场移动星体和飞船
    move(all.stars, all.spaceships, all.momentum_weapon, 0.1)

    # 操作系统接收键盘输入
    # if_continue, all.spaceships[0], all.momentum_weapon, all.scale, all.last_creation_time_0, all.last_presstime_0 = handle_key_0(
    #     key, all.spaceships[0], all.momentum_weapon, all.scale, all.last_creation_time_0, all.last_presstime_0)

    
    all.spaceships, all.momentum_weapon = destroy(all.spaceships, all.momentum_weapon)

    ###现在还没有加上q的功能###

    return all    

