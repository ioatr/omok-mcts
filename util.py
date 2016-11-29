import math
import numpy as np

BOARD_SIZE = 15
MAX_HAZARD = math.exp(5)

def get_at(board, x, y):
    return board[y * BOARD_SIZE + x]

def wincheck(board, pos, side):
    x = pos % BOARD_SIZE
    y = int (pos / BOARD_SIZE)

    def check_inner(x, y):
        return (x >= 0) and (y >= 0) and (x < BOARD_SIZE) and (y < BOARD_SIZE)

    def _check(board, x, y, dx, dy):
        count = 0
        while check_inner(x-dx, y-dy) and (get_at(board, x-dx, y-dy) == side):
            x, y = x-dx, y-dy
        while check_inner(x, y) and (get_at(board, x, y) == side):
            count+=1
            x, y = x+dx, y+dy
        if (count == 5):
            return True

    if _check(board, x, y, 1, 0):
        return True
    if _check(board, x, y, 0, 1):
        return True
    if _check(board, x, y, 1, 1):
        return True
    if _check(board, x, y, -1, 1):
        return True

    return False
 

def GetFavorableValue(map, nX, nY, Type):
    x, y, count, hazard = nX, nY, 0, 0 
    Map = np.copy(map)
    
    Map[nY * BOARD_SIZE + nX] = Type

    while (x > 0) and (get_at(Map, x-1,y) == Type):
        x-=1
    while (x < BOARD_SIZE) and (get_at(Map, x, y) == Type):
        count+=1
        x+=1
    if (count > 5):
        count = 2
    hazard += math.exp(count) / MAX_HAZARD

    x, y, count = nX, nY, 0  

    while (y > 0) and (get_at(Map, x, y-1) == Type):
        y-=1
    while (y < BOARD_SIZE) and (get_at(Map, x, y) == Type):
        count+=1
        y+=1
    if (count > 5):
        count = 2
    hazard += math.exp(count) / MAX_HAZARD

    x, y, count = nX, nY, 0
    while (x > 0) and (y > 0) and (get_at(Map, x-1, y-1) == Type):
        x-=1
        y-=1
    while (x < BOARD_SIZE) and (y < BOARD_SIZE) and (get_at(Map, x, y) == Type):
        count+=1
        x+=1
        y+=1
    if (count > 5):
        count = 2
    hazard += math.exp(count) / MAX_HAZARD

    x, y, count = nX, nY, 0
    while (x < BOARD_SIZE-1) and (y > 0) and (get_at(Map, x+1, y-1) == Type):
        x+=1
        y-=1
    while (x >= 0) and (y < BOARD_SIZE) and (get_at(Map, x, y) == Type):
        count+=1
        x-=1
        y+=1
    if (count > 5):
        count = 2
    hazard += math.exp(count) / MAX_HAZARD

    return min(1, hazard)