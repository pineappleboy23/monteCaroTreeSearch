import grid
import copy
import numpy as np


def MCTS(root, board, n_sims):
    expand_threshold = 1
    for _ in range(n_sims):
        b = grid.Grid(data=copy.deepcopy(board.grid), pieces=copy.deepcopy(board.pieces))
        cur_node = root
        while cur_node.visits >= expand_threshold:
            if cur_node.expanded:
                if cur_node.is_player:
                    # pick best scored move node
                    pass
                else:
                    #pick child (set of three blocks)
                    pass
            elif np.max(b.data) >= 2:
                break
            else:
                cur_node.expand(b)
        rollout
        backprop



# __init__(parent, total_score, visits, is_player, block, blocks, seed)
root = grid.Node(parent=None, total_score=0, visits=0, is_player=True, )