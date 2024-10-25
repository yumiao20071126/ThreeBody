import numpy as np
from ThreeBody_algorithm import star
import time
import keyboard
import cv2

#这个文件包含了游戏的操作函数，包括键盘操作和鼠标操作（暂时没有鼠标操作）
###这个函数中，last_creation_time和last_presstime用来记录每个按键的单机时刻###
###它们是一个数组存储了多个时刻数据，这样的设计显然是不合理的，但是在按键种类比较少的时候是可以接受的###
###在按键种类增多的时候，可以考虑用一个字典来存储，键是按键，值是时间###

def handle_key_0(key, spaceship0, momentum_weapon, scale, last_creation_time,last_presstime):
    #记录现在的时间，防止连续按键
    current_time = time.time()

    #按q退出游戏
    if key == ord('q'):
        return False, spaceship0, scale
    #按z放大
    elif key == ord('z'):
        scale = scale * 1.25
    #按x缩小
    elif key == ord('x'):
        scale = scale * 0.8


    #按w向前方加速，前方为飞船的速度方向
    if key == ord('w'):
        
        ###这一段操作系统可以改动###
        ###现在的移动系统需要每两次按键时间间隔超过一秒才有效###
        ###如果每次加速可以设置energy cost的话，可以改成每次加速都有效，删掉时间间隔部分###

        #如果两次按键的时间间隔大于1s，且两次按键的时间间隔大于0.1s，才能继续加速
        time_diff=current_time-last_creation_time[0]

        time_release=current_time-last_presstime[0]
        if time_diff>=1 and time_release>=0.1:
            v = np.sqrt(spaceship0.vx**2 + spaceship0.vy**2)
            spaceship0.vx = spaceship0.vx + spaceship0.vx / v
            spaceship0.vy = spaceship0.vy + spaceship0.vy / v

            #更新上一次的按键时间
            last_creation_time[0]=current_time
        last_presstime[0]=current_time
    #按s向后方加速，前方为飞船的速度方向
    elif key == ord('s'):
        time_diff=current_time-last_creation_time[1]
        time_release=current_time-last_presstime[1]
        if time_diff>=1 and time_release>=0.1:
            v = np.sqrt(spaceship0.vx**2 + spaceship0.vy**2)
            spaceship0.vx = spaceship0.vx - spaceship0.vx / v
            spaceship0.vy = spaceship0.vy - spaceship0.vy / v
            last_creation_time[1]=current_time
        last_presstime[1]=current_time
    #按d向右方加速，前方为飞船的速度方向
    elif key == ord('d'):
        time_diff=current_time-last_creation_time[2]
        time_release=current_time-last_presstime[2]
        if time_diff>=1 and time_release>=0.1:
            v = np.sqrt(spaceship0.vx**2 + spaceship0.vy**2)
            spaceship0.vx = spaceship0.vx + spaceship0.vy / v
            spaceship0.vy = spaceship0.vy - spaceship0.vx / v
            last_creation_time[2]=current_time
        last_presstime[2]=current_time
    #按a向左方加速，前方为飞船的速度方向
    elif key == ord('a'):
        time_diff=current_time-last_creation_time[3]
        time_release=current_time-last_presstime[3]
        if time_diff>=1 and time_release>=0.1:
            v = np.sqrt(spaceship0.vx**2 + spaceship0.vy**2)
            spaceship0.vx = spaceship0.vx - spaceship0.vy / v
            spaceship0.vy = spaceship0.vy + spaceship0.vx / v
            last_creation_time[3]=current_time
        last_presstime[3]=current_time

    #按e发射动量武器
    elif key==ord('e'):
        #记录上次发射的时间
        time_diff=current_time-last_creation_time[4]

        #记录上次按键的时间
        time_release=current_time-last_presstime[4]

        #两次按键的时间间隔大于1s，才允许继续发射，防止连续按键
        if time_diff>=1 and time_release>=1:

            #发射动量武器，调用发射函数
            momentum_weapon=add_spaceship(momentum_weapon, spaceship0)
            last_creation_time[4]=current_time
        last_presstime[4]=current_time

    return True, spaceship0,momentum_weapon, scale, last_creation_time, last_presstime


#以下函数是一个镜像操作系统，在两台机器联机还未实现时，可以用这个函数来操作第二台飞船
#用来测试代码
def handle_key_1(key, spaceship1, momentum_weapon, scale, last_creation_time,last_presstime):
    current_time = time.time()
    if key == ord('q'):
        return False, spaceship1, scale
    elif key == ord('m'):
        scale = scale * 1.25
    elif key == ord(','):
        scale = scale * 0.8

    if key == ord('i'):
        time_diff=current_time-last_creation_time[0]
        time_release=current_time-last_presstime[0]
        if time_diff>=1 and time_release>=0.1:
            v = np.sqrt(spaceship1.vx**2 + spaceship1.vy**2)
            spaceship1.vx = spaceship1.vx + spaceship1.vx / v
            spaceship1.vy = spaceship1.vy + spaceship1.vy / v
            last_creation_time[0]=current_time
        last_presstime[0]=current_time
    elif key == ord('k'):
        time_diff=current_time-last_creation_time[1]
        time_release=current_time-last_presstime[1]
        if time_diff>=1 and time_release>=0.1:
            v = np.sqrt(spaceship1.vx**2 + spaceship1.vy**2)
            spaceship1.vx = spaceship1.vx - spaceship1.vx / v
            spaceship1.vy = spaceship1.vy - spaceship1.vy / v
            last_creation_time[1]=current_time
        last_presstime[1]=current_time
    elif key == ord('l'):
        time_diff=current_time-last_creation_time[2]
        time_release=current_time-last_presstime[2]
        if time_diff>=1 and time_release>=0.1:
            v = np.sqrt(spaceship1.vx**2 + spaceship1.vy**2)
            spaceship1.vx = spaceship1.vx + spaceship1.vy / v
            spaceship1.vy = spaceship1.vy - spaceship1.vx / v
            last_creation_time[2]=current_time
        last_presstime[2]=current_time
    elif key == ord('j'):
        time_diff=current_time-last_creation_time[3]
        time_release=current_time-last_presstime[3]
        if time_diff>=1 and time_release>=0.1:
            v = np.sqrt(spaceship1.vx**2 + spaceship1.vy**2)
            spaceship1.vx = spaceship1.vx - spaceship1.vy / v
            spaceship1.vy = spaceship1.vy + spaceship1.vx / v
    elif key==ord('o'):
        time_diff=current_time-last_creation_time[4]
        time_release=current_time-last_presstime[4]
        if time_diff>=1 and time_release>=1:
            momentum_weapon=add_spaceship(momentum_weapon, spaceship1)
            last_creation_time[4]=current_time
        last_presstime[4]=current_time
    return True, spaceship1,momentum_weapon, scale, last_creation_time, last_presstime


#这个函数是用来发射动量武器的，发射的动量武器的速度是飞船的速度加上一个固定的速度
def add_spaceship(momentum_weapon,spaceship0):
    v=np.sqrt(spaceship0.vx**2+spaceship0.vy**2)
    delta_vx=30*spaceship0.vx/v
    delta_vy=30*spaceship0.vy/v
    momentum_piece=star(spaceship0.x, spaceship0.y, spaceship0.vx+delta_vx, spaceship0.vy+delta_vy,0)
    
    #发射的动量武器将被存储在一个数组之中
    momentum_weapon.append(momentum_piece)
    return momentum_weapon