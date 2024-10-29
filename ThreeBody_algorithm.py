#ThreeBody

import numpy as np
import time

#这个文件包含了最基本的平方反比引力公式

#恒星类，包含坐标和速度和质量，飞船类似，只不过会将m设为0
class star:
    def __init__(self, x, y, vx, vy, m,name='star'):
        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.m = m

        self.name=name

#计算两颗星之间的引力加速度
def Gravity(star_1, star_2, dt):
    dx = star_2.x - star_1.x
    dy = star_2.y - star_1.y
    r2=dx**2+dy**2
    
    #Distance squared
    r = np.sqrt(r2)
    #Gravitational constant
    G = 1
    #Gravitational force
    a = G * star_2.m / r**2
    #Gravitational acceleration
    ax = a * dx / r 
    ay = a * dy / r 
    #Update velocities

    star_1.vx += ax * dt
    star_1.vy += ay * dt

    # star_2.vx -= ax * dt
    # star_2.vy -= ay * dt
    return star_1


#根据每个星体（飞船）的速度，更新位置
def velocity(star,star_, dt):
    star.x += (star.vx+star_.vx) * dt/2
    star.y += (star.vy+star_.vy) * dt/2
    return star

