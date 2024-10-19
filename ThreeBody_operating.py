import numpy as np
from ThreeBody_algorithm import star
import time
import keyboard
import cv2

#不能再一秒钟内创建两艘飞船
#spaceships是一个列表，存储所有飞船的信息

#momentum_weapon=[]
def handle_key(key, spaceship0, momentum_weapon, scale, last_creation_time,last_presstime):
    current_time = time.time()
    if key == ord('q'):
        return False, spaceship0, scale
    elif key == ord('z'):
        scale = scale * 1.25
    elif key == ord('x'):
        scale = scale * 0.8



    if key == ord('w'):
        time_diff=current_time-last_creation_time[0]
        time_release=current_time-last_presstime[0]
        if time_diff>=1 and time_release>=0.2:
            v = np.sqrt(spaceship0.vx**2 + spaceship0.vy**2)
            spaceship0.vx = spaceship0.vx + spaceship0.vx / v
            spaceship0.vy = spaceship0.vy + spaceship0.vy / v
            last_creation_time[0]=current_time
        last_presstime[0]=current_time
    elif key == ord('s'):
        time_diff=current_time-last_creation_time[1]
        time_release=current_time-last_presstime[1]
        if time_diff>=1 and time_release>=0.2:
            v = np.sqrt(spaceship0.vx**2 + spaceship0.vy**2)
            spaceship0.vx = spaceship0.vx - spaceship0.vx / v
            spaceship0.vy = spaceship0.vy - spaceship0.vy / v
            last_creation_time[1]=current_time
        last_presstime[1]=current_time
    elif key == ord('d'):
        time_diff=current_time-last_creation_time[2]
        time_release=current_time-last_presstime[2]
        if time_diff>=1 and time_release>=0.2:
            v = np.sqrt(spaceship0.vx**2 + spaceship0.vy**2)
            spaceship0.vx = spaceship0.vx + spaceship0.vy / v
            spaceship0.vy = spaceship0.vy - spaceship0.vx / v
            last_creation_time[2]=current_time
        last_presstime[2]=current_time
    elif key == ord('a'):
        time_diff=current_time-last_creation_time[3]
        time_release=current_time-last_presstime[3]
        if time_diff>=1 and time_release>=0.2:
            v = np.sqrt(spaceship0.vx**2 + spaceship0.vy**2)
            spaceship0.vx = spaceship0.vx - spaceship0.vy / v
            spaceship0.vy = spaceship0.vy + spaceship0.vx / v
            last_creation_time[3]=current_time
        last_presstime[3]=current_time
    elif key==ord('e'):
        time_diff=current_time-last_creation_time[4]
        time_release=current_time-last_presstime[4]
        if time_diff>=1 and time_release>=1:
            momentum_weapon=add_spaceship(momentum_weapon, spaceship0)
            last_creation_time[4]=current_time
        last_presstime[4]=current_time

    return True, spaceship0,momentum_weapon, scale, last_creation_time, last_presstime

def add_spaceship(momentum_weapon,spaceship0):
    v=np.sqrt(spaceship0.vx**2+spaceship0.vy**2)
    delta_vx=30*spaceship0.vx/v
    delta_vy=30*spaceship0.vy/v
    momentum_piece=star(spaceship0.x, spaceship0.y, spaceship0.vx+delta_vx, spaceship0.vy+delta_vy,0)
    
    momentum_weapon.append(momentum_piece)
    return momentum_weapon