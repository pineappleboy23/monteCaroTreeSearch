import grid
import copy
import numpy as np
import random


def expand(node, game):
    amount_of_3_random_pieces = 80
    if len(node.blocks) == 0:
        for i in range(amount_of_3_random_pieces):
            pieces = game.generate_3_pieces()

            # __init__(self, parent, total_score, visits, is_player, block=None, blocks=None, seed=None, position=None)
            node.children.append(grid.Node(node, 0, 0, False, block=None, blocks=pieces))
    else:
        for i in range(len(node.blocks)):
            for position in game.possible_moves(node.blocks[i]):
                # __init__(self, parent, total_score, visits, is_player, block=None, blocks=None, seed=None, position=None)
                new_pieces = [pp.copy() for pp in node.blocks]
                new_pieces.pop(i)
                node.children.append(
                    grid.Node(node, 0, 0, True, block=node.blocks[i].copy(), blocks=new_pieces, position=position))
    node.expanded = True


def update(node, board):
    if node.is_player:
        board.add_piece(node.block.copy(), node.position[0], node.position[1])
    board.pieces = copy.deepcopy(node.blocks)
    board.no_moves_left()


def rollout_and_backprop(node, game):
    # play out random game
    while not game.random_move()[0]:
        pass

    score = game.score

    # backprop to update scores and visits
    cur_node = node
    while cur_node.parent is not None:
        cur_node.total_score += score
        cur_node.visits += 1

        cur_node.update_UTC()

        cur_node = cur_node.parent

    # update root visits
    cur_node.visits += 1


def MCTS(root, board, n_sims):
    expand_threshold = 1
    for sim_count in range(n_sims):
        if sim_count % 1000 == 0:
            print(sim_count)
        b = grid.Grid(data=copy.deepcopy(board.data), pieces=copy.deepcopy(root.blocks))
        cur_node = root
        while cur_node.visits >= expand_threshold:
            if cur_node.expanded:
                # if kid is player, sample using UTC
                if cur_node.children[0].is_player:
                    # pick best scored move node
                    index = np.argmax([c.UTC for c in cur_node.children])
                    cur_node = cur_node.children[index]
                else:
                    cur_node = random.choice(cur_node.children)
                update(cur_node, b)
            elif np.max(b.data) >= 2 or b.no_moves_left():
                break
            else:
                expand(cur_node, b)

        rollout_and_backprop(cur_node, b)

    best_node_index = np.argmax([c.UTC for c in root.children])
    best_node = root.children[best_node_index]

    return best_node

def print_colored_grid(grid):

    for row in grid:
        for cell in row:
            if cell == 1:
                print('\033[41m  \033[0m', end='')  # Red block
            else:
                print('\033[44m  \033[0m', end='')  # Blue block
        print()  # New line for each row
    print(11111111111111111111111111111)



random.seed(1)

start_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],

]

start_grid = [
    [0, 1, 0, 1, 1, 1, 0, 0],
    [0, 1, 0, 1, 1, 0, 0, 1],
    [0, 0, 0, 0, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0],
]

start_blocks = [
[
    [1, 1, 1],
    [0, 0, 1],
    [0, 0, 1]
],

    np.ones((4,1))
,

        np.ones((2,1))


]

start_blocks = [
[
    [1],
    [1]

],

    [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
,

    [
        [1],
        [1]
    ]


]

game = grid.Grid()

#game.add_piece(start_grid, 0, 0)

#game.pieces = start_blocks

#print_colored_grid(start_grid)
#for bbb in start_blocks:
#    print_colored_grid(bbb)

# game.give_board_pieces()

# __init__(self, parent, total_score, visits, is_player, block=None, blocks=None, seed=None, position=None)
root = grid.Node(parent=None, total_score=0, visits=0, is_player=False, blocks=game.pieces)

while not game.no_moves_left():
    root = MCTS(root, game, 7_000)
    # clean up parent tree data?
    if root.is_player:
        game.add_piece(root.block.copy(), root.position[0], root.position[1])
    game.pieces = copy.deepcopy(root.blocks)

    print("--------------------")
    print(root.position)
    print_colored_grid(game.data)
    print(game.score)
    print("--------")
    for i in root.blocks:
        print(i)
    print("--------------------")

    # cleanup of old tree nodes to free memory
    root.parent.children = []
    root.parent = None

for i in range(8):
    print(game.data[i])
print(game.score)
