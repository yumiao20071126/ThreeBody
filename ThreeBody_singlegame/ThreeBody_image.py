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

#这个文件包含了游戏所有的图形化功能

###在以下的代码中会涉及到scale和bias_x,bias_y，它们是放大倍率和偏移量，可以使用操作系统改变它们的值###
#画星体

def draw_star(frame, star,scale,bias_x,bias_y):
    
    x_image = int(star.x*scale + 500+bias_x)
    y_image = int(star.y*scale + 500+bias_y)
    r=int(np.sqrt(star.m)*scale/10)
    if(r<5):
        r=5
    cv2.circle(frame, (x_image, y_image), r, (0, 255, 255), -1)
    return frame

#画飞船
def draw_spaceship(frame, spaceship, scale, bias_x, bias_y):
    x_image = int(spaceship.x*scale + 500+bias_x)
    y_image = int(spaceship.y*scale + 500+bias_y)
    
    ###在测试阶段飞船暂时被画成了一个半径为5的白色圆圈###       
    r=5
    cv2.circle(frame, (x_image, y_image), r, (255, 255, 255), -1)
    return frame

#画动量武器（碎片）
def draw_momentum_weapon(frame, momentum_piece, scale, bias_x, bias_y):
    x_image = int(momentum_piece.x*scale + 500+bias_x)
    y_image = int(momentum_piece.y*scale + 500+bias_y)
    
    ###在测试阶段动量武器（碎片）暂时被画成了一个半径为5的灰色圆圈###
    r=5
    cv2.circle(frame, (x_image, y_image), r, (180, 180, 180), -1)
    return frame

#画枪瞄
def gun_sight(frame, spaceships, scale, bias_x, bias_y):
    #这个函数会在飞船的路径延长线上画一段直线，用于预计飞船的飞行路径和动量武器的飞行路径
    for i in range(0, len(spaceships)):
        v=np.sqrt(spaceships[i].vx**2+spaceships[i].vy**2)
        theta_x=spaceships[i].vx/v
        theta_y=spaceships[i].vy/v
        
        for j in range(0,50) :
            sight_x=spaceships[i].x+theta_x*j*(20+j)
            sight_y=spaceships[i].y+theta_y*j*(20+j)
            x_image=int(sight_x*scale + 500+bias_x)
            y_image=int(sight_y*scale+500+bias_y)
            if 0<x_image<1000:
                if 0<y_image<1000:
                    frame[y_image][x_image]=(255,255,255)

#整合上面的所有函数，更新帧
def DrawImage(frame,stars,spaceships, momentum_weapon, scale,bias_x,bias_y):
    for i in range(0, len(stars)):
        
        frame=draw_star(frame, stars[i],scale,bias_x,bias_y)
    for i in range(0, len(spaceships)):
        frame=draw_spaceship(frame, spaceships[i],scale,bias_x,bias_y)

    for i in range(0, len(momentum_weapon)):
        frame=draw_momentum_weapon(frame, momentum_weapon[i],scale,bias_x,bias_y)

    #画一个红色的矩形框，用于标记游戏的边界
    top_left = (int((3000) * scale + 500 + bias_x), int((-3000) * scale + 500 + bias_y ))
    bottom_right = (int((-3000) * scale + 500 + bias_x), int((3000) * scale + 500 + bias_y))
    cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)
    gun_sight(frame, spaceships, scale, bias_x, bias_y)

    #返回更新后的帧
    return frame
