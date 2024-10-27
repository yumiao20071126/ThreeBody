#ThreeBody_movements
import numpy as np
# from ThreeBody_algorithm import Gravity
import copy
import threading
from ThreeBody_algorithm import Gravity
from ThreeBody_algorithm import star
from ThreeBody_algorithm import velocity

#这个文件将调用平方反比引力公式，更新各个星体和和飞船和武器的位置

#计算一颗星体受到的所有其他星体的引力
def move_one_star(star,stars, dt):
    for i in range(0, len(stars)):
        if stars[i] != star:
            star=Gravity(star, stars[i], dt)
    return star
###在现在的程序中，这个函数没有被应用，可以注释掉，因为每个星体都会受到其他星体的引力，所以不需要单独计算###

#计算所有星体受到的引力
#更新星体，飞船，动量武器的位置
def move(stars, spaceships, momentum_weapon, dt):
    stars_=copy.deepcopy(stars)
    for i in range(0, len(stars)):
        # stars[i]=move_one_star(stars[i], stars, dt)
        for j in range(0, len(stars)):
            if j!=i:
                
                stars[i]=Gravity(stars[i], stars[j], dt)

    for i in range(0, len(stars)):
        stars[i]=velocity(stars[i], stars[i],dt)

    move_spaceships(spaceships, stars, dt)
    move_momentum_weapon(momentum_weapon, stars, dt)
    return stars, spaceships, momentum_weapon

#更新飞船的位置，只需要计算各个恒星对飞船的引力
def move_spaceships(spaceships, stars, dt):

    for i in range(0, len(stars)):
        # stars[i]=move_one_star(stars[i], stars, dt)
        for j in range(0, len(spaceships)):
           spaceships[j]=Gravity(spaceships[j], stars[i], dt)
    for i in range(0, len(spaceships)):
        spaceships[i]=velocity(spaceships[i], spaceships[i],dt)
    return spaceships

#更新动量武器的位置，只需要计算各个恒星对动量武器的引力
def move_momentum_weapon(momentum_weapon, stars, dt):
    for i in range(0, len(stars)):
        # stars[i]=move_one_star(stars[i], stars, dt)
        for j in range(0, len(momentum_weapon)):
           momentum_weapon[j]=Gravity(momentum_weapon[j], stars[i], dt)
    #print(len(momentum_weapon))
    if len(momentum_weapon)==0:
        return momentum_weapon
    else:
        print(momentum_weapon[0].x)
        for i in range(0, len(momentum_weapon)):
            momentum_weapon[i]=velocity(momentum_weapon[i], momentum_weapon[i],dt)
        print(momentum_weapon[0].x)

    return momentum_weapon
    