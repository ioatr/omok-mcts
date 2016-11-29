import random
import math
import numpy as np
import time
import sys
from util import *

class Node():
    def __init__(self, board, move, side, parent=None):
        
        board[move] = side

        self.board=board
        self.move=move
        self.side=side
        
        self.children=[]
        self.parent=parent

        def get_depth(node):
            depth = 0
            while node.parent:
                depth += 1
                node = node.parent
            return depth

        self.depth = get_depth(self)

        if wincheck(board, move, side):
            self.next_moves = []
            self.terminal = True
            self.w = 1
            self.n = 1
        else:
            # get next move position
            # neighbor of stones
            self.next_moves = []
            for i, stone in enumerate(board):
                if stone == 0:
                    def is_sibling_stone(board, move):
                        cx = move % BOARD_SIZE
                        cy = int(move / BOARD_SIZE)
                    
                        for dy in [-1, 0, 1]:
                            for dx in [-1, 0, 1]:
                                x = min(max(0, cx + dx), BOARD_SIZE-1)
                                y = min(max(0, cy + dy), BOARD_SIZE-1) 
                                
                                if board[y * BOARD_SIZE + x] != 0:
                                    return True

                        return False
                    if is_sibling_stone(board, i):
                        self.next_moves.append(i)

            if len(self.next_moves) == 0:
                # draw
                self.terminal = True
                self.w = 0
                self.n = 1
            else:
                self.terminal = False
                self.w = 0
                self.n = 0

    def is_terminal(self):
        return self.terminal
    
    def is_win(self):
        return self.w > 0

    def fully_expanded(self):
        if (len(self.children) == len(self.next_moves)):
            return True
        return False

    def opponent_side(self):
        return self.side * -1

    def get_unexpanded_child(self):
        tried_moves=[c.move for c in self.children]
        for move in self.next_moves:
            if move not in tried_moves:
                child = Node(np.copy(self.board), move, self.opponent_side(), self)
                self.children.append(child)
                return child

        raise Exception('can not find unexpanded node')


SCALAR = math.sqrt(2)

def SELECTION(node):

    #min-max tree selection for turn game
    is_max = ((node.depth % 2) == 1)

    best_value = -1e6 if is_max else 1e6
    best_children = []
    assert(len(node.children) > 0)

    for c in node.children:
        # Exploration and exploitation in https://en.wikipedia.org/wiki/Monte_Carlo_tree_search 
        value = (c.w / c.n) + SCALAR * math.sqrt(math.log(node.n)/c.n)
        if value == best_value:
            best_children.append(c)

        if is_max:
            # MAX step
            if value > best_value:
                best_value = value
                best_children = [c]
        else:
            # MIN step
            if value < best_value:
                best_value = value
                best_children = [c]
    
    assert(len(best_children) > 0)

    return random.choice(best_children)


def EXPANSION(node):
    child = node.get_unexpanded_child()
    # ...
    return child

def SIMULATION2(node):
    assert(len(node.children) == 0)

    if node.is_terminal():
        if(node.depth % 2) == 0:
            if node.is_win() == True:
                return 1
        
    else:
        if (node.depth % 2) == 0:
            side = node.side
            x = node.move % BOARD_SIZE
            y = int(node.move / BOARD_SIZE)
        
            score = GetFavorableValue(node.board, x, y, node.side)
            return score

    return 0
    
def SIMULATION(node):
    
    assert(len(node.children) == 0)
    
    board = np.copy(node.board)
    
    # roll out the game
    while node.is_terminal() == False:
        # make  random
        side = node.opponent_side()
        move = random.choice(node.next_moves)
        node = Node(board, move, side, node)

    if node.is_win() == True:
        # score only at my turn
        if(node.depth % 2) == 0:
            return 1
        else:
            return 0

    return 0

def BACKPROPAGATION(node, score):
    #TODO : apply min-max tree 
    while node != None:
        node.n += 1
        node.w += score
        node = node.parent

def MCTS(root, limit_time):
    # sampling step
    
    is_max = True
    start_time = time.time()
    loop = 0

    # loop until limit time
    while (time.time() - start_time) < limit_time:
        node = root
        while node.is_terminal() == False:
            if node.fully_expanded():
                # fully expanded, so choose best scored node
                # find by min-max tree search
                node = SELECTION(node)
            else:
                # expand node
                child = EXPANSION(node)
                # scoring node
                score = SIMULATION2(child)
                # backpropagation to parent
                BACKPROPAGATION(child, score)
                break

        loop += 1

    print('MCTS loop = %d, time=%f' % (loop, (time.time() - start_time)))
    # select best
    return SELECTION(root)
    
if __name__ == '__main__':

    def OPPONENT_TURN(node, move):
        for child in node.children:
            if child.move == move:
                return child
        
        new_board = np.copy(node.board)
        new_side = node.opponent_side()
        new_move = random.choice(node.next_moves)
        new_node = Node(new_board, new_move, new_side, node)
        node.children.append(new_node)
        if new_node.is_terminal() == False:
            score = SIMULATION(new_node)
            # backpropagation to parent
            BACKPROPAGATION(new_node, score)
        

        return new_node

    def o_print(node):
        for i, stone in enumerate(node.board):
            if stone == 1:
                sys.stdout.write('X')
            elif stone == -1:
                sys.stdout.write('O')
            else:
                sys.stdout.write(' ')

            if i % BOARD_SIZE == BOARD_SIZE - 1: 
                sys.stdout.write('\r\n')
        sys.stdout.flush()


    BLACK = 1
    WHILTE = -1
    board = np.zeros((BOARD_SIZE*BOARD_SIZE), dtype=np.int8)
    root = Node(board, 7*BOARD_SIZE + 7, BLACK)
    o_print(root)
    node = root
    while not node.is_terminal():
        enemy_move = random.choice(node.next_moves)
        node = OPPONENT_TURN(node, enemy_move)
        node = MCTS(node, 10)
        o_print(node)
    