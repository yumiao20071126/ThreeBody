import cv2
import numpy as np
# from ThreeBody_algorithm import Gravity
import time
import threading
from ThreeBody_movements import move
from ThreeBody_algorithm import star

frame=None

def draw_circle(frame, star):
    x_image = int(star.x + 500)
    y_image = int(star.y + 500)
    r=int(np.sqrt(star.m)/10)
    cv2.circle(frame, (x_image, y_image), r, (0, 255, 255), -1)
    return frame

def DrawImage(frame,stars):
    for i in range(0, len(stars)):
        frame=draw_circle(frame, stars[i])
    return frame

def main():
    # 初始条件
    n=2
    star_1=star(100, 0.0, -2.5, 5, 10000)
    star_2=star(-200, 0.0, -2.5, -5, 10000)
    star_3=star(50.0, -50.0, 5, 0.0, 10000)
    stars=[star_1, star_2, star_3]


    # move(stars)
    # 视频参数
    width, height = 1000, 1000
    # 创建一个黑色背景的帧
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    for i in range(10000):
        # 计算当前帧中点的位置
        
        move(stars, 0.1)
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame=DrawImage(frame,stars)

        # 显示帧
        cv2.imshow('Moving Dot', frame)

        # 等待一段时间以控制帧率
        if cv2.waitKey(int(10)) & 0xFF == ord('q'):
            
            break

if __name__ == '__main__':
    main()


