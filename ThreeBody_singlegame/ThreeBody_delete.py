#ThreeBody_delete

import sys
import os

#这个文件定义了飞船出界规则，如果飞船出界，就删除飞船
###暂定飞船出界规则为飞船的坐标超过3000或者小于-3000就删除飞船###

def delete_spaceship(spaceships):
    for spaceship in spaceships:
    
        if spaceship.x>3000:
            spaceships.remove(spaceship)
        if spaceship.y>3000:
            spaceships.remove(spaceship)
        if spaceship.x<-3000:
            spaceships.remove(spaceship)
        if spaceship.y<-3000:
            spaceships.remove(spaceship)
    return spaceships

def remove_momentum_pieces(momentum_weapon):
    for momentum_piece in momentum_weapon:
        if momentum_piece.x>3000:
            momentum_weapon.remove(momentum_piece)
        if momentum_piece.y>3000:
            momentum_weapon.remove(momentum_piece)
        if momentum_piece.x<-3000:
            momentum_weapon.remove(momentum_piece)
        if momentum_piece.y<-3000:
            momentum_weapon.remove(momentum_piece)
    return momentum_weapon


#在这里定义delete函数整合各个模块的删除程序
def delete(stars,spaceships, momentum_weapon):
    delete_spaceship(spaceships)
    remove_momentum_pieces(momentum_weapon)
    return stars,spaceships, momentum_weapon
    