#ThreeBody

import numpy as np
import time
class star:
    def __init__(self, x, y, vx, vy, m):
        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.m = m

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

# def ThreeBody(x0, y0, z0, vx0, vy0, vz0, dt, n):
def velocity(star,star_, dt):
    star.x += (star.vx+star_.vx) * dt/2
    star.y += (star.vy+star_.vy) * dt/2
    return star

