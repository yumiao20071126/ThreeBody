import cv2
import numpy as np
# from ThreeBody_algorithm import Gravity
import time
import threading
from ThreeBody_movements import move
from ThreeBody_algorithm import star
import keyboard
from ThreeBody_operating import handle_key
frame=None

def draw_star(frame, star,scale,bias_x,bias_y):
    # print(star.x)
    x_image = int(star.x*scale + 500+bias_x)
    y_image = int(star.y*scale + 500+bias_y)
    r=int(np.sqrt(star.m)*scale/10)
    if(r<5):
        r=5
    cv2.circle(frame, (x_image, y_image), r, (0, 255, 255), -1)
    return frame

def draw_spaceship(frame, spaceship, scale, bias_x, bias_y):
    x_image = int(spaceship.x*scale + 500+bias_x)
    y_image = int(spaceship.y*scale + 500+bias_y)
    
    r=5
    cv2.circle(frame, (x_image, y_image), r, (255, 255, 255), -1)
    return frame

def draw_momentum_weapon(frame, momentum_piece, scale, bias_x, bias_y):
    x_image = int(momentum_piece.x*scale + 500+bias_x)
    y_image = int(momentum_piece.y*scale + 500+bias_y)
    
    r=5
    cv2.circle(frame, (x_image, y_image), r, (180, 180, 180), -1)
    return frame

def DrawImage(frame,stars,spaceships, momentum_weapon, scale,bias_x,bias_y):
    for i in range(0, len(stars)):
        
        frame=draw_star(frame, stars[i],scale,bias_x,bias_y)
    for i in range(0, len(spaceships)):
        frame=draw_spaceship(frame, spaceships[i],scale,bias_x,bias_y)
    print(len(momentum_weapon))
    for i in range(0, len(momentum_weapon)):
        frame=draw_momentum_weapon(frame, momentum_weapon[i],scale,bias_x,bias_y)
    top_left = (int((3000) * scale + 500 + bias_x), int((-3000) * scale + 500 + bias_y ))
    bottom_right = (int((-3000) * scale + 500 + bias_x), int((3000) * scale + 500 + bias_y))
    cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)
    return frame

def abs(x):
    if x<0:
        return -x
    else:
        return x

def main():
    # 初始条件
    star_1=star(300, 0.0, 0, 1, 10000)
    star_2=star(-300, 0.0, 0, -1, 10000)
    spaceship0=star(50.0, 500.0, 0, 0,0)
    stars=[star_1, star_2]
    spaceship1=star(-50, 500.0, 0.0, 0.0, 0.0)
    spaceships=[]
    momentum_weapon=[]
    spaceships.append(spaceship0)
    spaceships.append(spaceship1)
    
    # 视频参数
    width, height = 1000, 1000
    # 创建一个黑色背景的帧
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    scale=1
    bias_x=0
    bias_y=0
    last_creation_time=[time.time(),time.time(),time.time(),time.time(),time.time()]
    last_presstime=[time.time(),time.time(),time.time(),time.time(),time.time()]
    for i in range(100000):
        # 计算当前帧中点的位置
        for spaceship in spaceships:
             # 在这里绘制一个 3000x3000 的空心长方形
            
            if(spaceship!=spaceship1):
                if(-10<=spaceship.x-spaceship1.x<=10):
                    if(-10<=spaceship.y-spaceship1.y<=10):
                        print(spaceship.x-spaceship1.x)
                        print(spaceship.y-spaceship1.y)
                        print("spaceship destroyed")
            if spaceship.x>3000:
                spaceships.remove(spaceship)
            if spaceship.y>3000:
                spaceships.remove(spaceship)
            if spaceship.x<-3000:
                spaceships.remove(spaceship)
            if spaceship.y<-3000:
                spaceships.remove(spaceship)
        for momentum_piece in momentum_weapon:
            if momentum_piece.x>3000:
                momentum_weapon.remove(momentum_piece)
            if momentum_piece.y>3000:
                momentum_weapon.remove(momentum_piece)
            if momentum_piece.x<-3000:
                momentum_weapon.remove(momentum_piece)
            if momentum_piece.y<-3000:
                momentum_weapon.remove(momentum_piece)
        print(len(momentum_weapon))
        print(len(spaceships))
        move(stars, spaceships, momentum_weapon, 0.1)
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame=DrawImage(frame,stars,spaceships, momentum_weapon,scale,bias_x,bias_y)

        # 显示帧
        cv2.imshow('Moving Dot', frame)

        # 等待一段时间以控制帧率
        

        key = cv2.waitKey(int(10)) & 0xFF
        #操作系统接收键盘输入
        if_continue, spaceship0, momentum_weapon, scale, last_creation_time, last_presstime=handle_key(key, spaceship0, momentum_weapon, scale,last_creation_time, last_presstime)
        if(if_continue==False):
            break
        

if __name__ == '__main__':
    main()



    # # 长方形的尺寸
    # length = 10
    # width = 20
    
    # # 计算旋转角度
    # angle = np.arctan2(spaceship.vy, spaceship.vx)
    
    # # 计算长方形的四个顶点
    # rect = np.array([
    #     [-length / 2, -width / 2],
    #     [length / 2, -width / 2],
    #     [length / 2, width / 2],
    #     [-length / 2, width / 2]
    # ])
    
    # # 旋转矩阵
    # rotation_matrix = np.array([
    #     [np.cos(angle), -np.sin(angle)],
    #     [np.sin(angle), np.cos(angle)]
    # ])
    
    # # 旋转并平移顶点
    # rect_rotated = np.dot(rect, rotation_matrix)
    # rect_rotated[:, 0] += x_image
    # rect_rotated[:, 1] += y_image
    
    # # 将顶点转换为整数
    # rect_rotated = rect_rotated.astype(int)
    
    # # 绘制长方形
    # cv2.polylines(frame, [rect_rotated], isClosed=True, color=(0, 255, 255), thickness=2)