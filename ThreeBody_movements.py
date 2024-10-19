#ThreeBody_movements
import numpy as np
# from ThreeBody_algorithm import Gravity
import copy
import threading
from ThreeBody_algorithm import Gravity
from ThreeBody_algorithm import star
from ThreeBody_algorithm import velocity

def move_one_star(star,stars, dt):
    for i in range(0, len(stars)):
        if stars[i] != star:
            star=Gravity(star, stars[i], dt)
    return star


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

def move_spaceships(spaceships, stars, dt):

    for i in range(0, len(stars)):
        # stars[i]=move_one_star(stars[i], stars, dt)
        for j in range(0, len(spaceships)):
           spaceships[j]=Gravity(spaceships[j], stars[i], dt)
    for i in range(0, len(spaceships)):
        spaceships[i]=velocity(spaceships[i], spaceships[i],dt)
    return spaceships

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
    