import sys
import os
import numpy as np
import matplotlib.pyplot as plt


#这个文件定义了卫星被碎片的摧毁规则，如果碎片的速度方向朝向卫星，则被摧毁
def destroy(spaceships, momentum_pieces):
    for spaceship in spaceships:
        for i in range(len(momentum_pieces)):
            delta_x=spaceship.x-momentum_pieces[i].x
            delta_y=spaceship.y-momentum_pieces[i].y
            s=(delta_x)**2+(delta_y)**2

            #如果碎片的速度方向朝向卫星，则被摧毁
            ###如果没有以下5行代码，飞船会发射动量武器（碎片），但在发射的时候碎片与飞船的距离是0，这会导致飞船直接被判定未被摧毁###
            v_n=momentum_pieces[i].vx*(delta_x)+momentum_pieces[i].vy*(delta_y)
            if s<100 and v_n>0:
                #将飞船移除出飞船数组
                momentum_pieces.remove(momentum_pieces[i])
                spaceships.remove(spaceship)
    return spaceships, momentum_pieces
    
