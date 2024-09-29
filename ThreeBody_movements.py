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


def move(stars, dt):
    stars_=copy.deepcopy(stars)
    for i in range(0, len(stars)):
        # stars[i]=move_one_star(stars[i], stars, dt)
        for j in range(0, len(stars)):
            if j!=i:
                
                stars[i]=Gravity(stars[i], stars[j], dt)

    for i in range(0, len(stars)):
        stars[i]=velocity(stars[i], stars[i],dt)
    
    return stars
