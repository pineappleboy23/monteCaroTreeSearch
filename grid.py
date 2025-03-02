import numpy as np
import random


# Manages a grid of values
class Grid():
    def __init__(self, width=8, height=8, default=0, data=None, pieces=[]):
        self.width = width
        self.height = height
        if data is None:
            self.data = np.array([[default for y in range(height)] for x in range(width)])
        else:
            self.data = data
        self.pieces = pieces
        self.score = 0

        self.game_ended = False

    def piece_fits(self, piece, x, y):
        piece_board = np.zeros((8, 8))

        for r in range(len(piece)):
            for c in range(len(piece[0])):
                # this allows us to add stuff that goes out of bounds as long as it's zero
                # and not aprt of the piece

                if 0 <= x + r < 8 and 0 <= y + c < 8:  # Ensure we don't go out of bounds
                    piece_board[x + r, y + c] = piece[r, c]
                else:
                    return False

        return np.max(piece_board + self.data) < 2

    def add_piece(self, piece, x, y):
        for r in range(len(piece)):
            for c in range(len(piece[0])):
                if 0 <= x + r < 8 and 0 <= y + c < 8:  # Ensure we don't go out of bounds
                    self.data[x + r, y + c] += piece[r, c]

        # add up score and remove filled rows and cols
        self.clear_lines()

    def give_board_pieces(self):
        if len(self.pieces) == 0:
            self.pieces = self.generate_3_pieces()
            return True
        return False

    def generate_3_pieces(self):
        p = []
        for i in range(3):
            p.append(random.choice(pieces).arr)
        return p

    def possible_moves(self, piece):
        moves = []

        # go up to 8 search because some pieces are 1 or 2 wide
        # piece fits will cover problems
        for x in range(9 - len(piece)):
            for y in range(9 - len(piece[0])):
                if self.piece_fits(piece, x, y):
                    moves.append((x, y))
        return moves

    # returns (game_ended, score)
    def random_move(self):
        if self.game_ended:
            return
        if len(self.pieces) == 0:
            self.pieces = self.generate_3_pieces()
            return (False, self.score)
        else:
            before_len = len(self.pieces)
            for i in range(len(self.pieces)):
                moves = self.possible_moves(self.pieces[i])
                if len(moves) > 0:
                    move = random.choice(moves)
                    piece_to_play = self.pieces.pop(i)
                    self.add_piece(piece_to_play, move[0], move[1])
                    break

            if before_len == len(self.pieces):
                self.game_ended = True
                return (True, self.score)

        return (False, self.score)

    # remove solid rows and columns here, do both at once
    def clear_lines(self):
        squares_to_reset = []

        for row in range(8):
            # if row is full
            if np.min(self.data[row]) == 1:
                # clear row and add to score
                squares_to_reset.extend([(row, y) for y in range(8)])
                self.score += 1

        # now clear columns
        # check for full columns
        for col in range(8):
            if np.min(self.data[:, col]) == 1:  # Column is full
                squares_to_reset.extend([(x, col) for x in range(8)])
                self.score += 1

        # clear the identified squares
        for x, y in squares_to_reset:
            self.data[x, y] = 0  # reset squares to empty


# Extension of the Grid class that can render to text and rotate
class DisplayableGrid(Grid):
    def __str__(self):
        return self.render()

    def render(self):
        res = []

        horiSplit = ' | '
        vertSplit = '\n +' + '---+' * self.width + '\n'

        for row in self.data:
            res.append(horiSplit + horiSplit.join(row) + horiSplit)

        return vertSplit + vertSplit.join(res) + vertSplit


class Piece():

    def __init__(self, shape):
        self.piece_shape = shape
        self.arr = self.to_array()

    def __str__(self):
        return self.render()

    def to_array(self):
        # Get the shape dimensions
        rows = len(self.piece_shape)
        cols = max(len(row) for row in self.piece_shape)

        # Initialize a 3x3 array with zeros
        array = np.zeros((rows, cols), dtype=int)

        # Fill in the "x" values with 1s
        for r, row in enumerate(self.piece_shape):
            for c, char in enumerate(row):
                if r < rows and c < cols:
                    array[r, c] = 1 if char == "x" else 0

        return array

    def render(self):
        res = []

        for row in self.piece_shape:
            res.append("".join(row) + "\n")

        return "".join(res)


pieces = [

    Piece([["x", "x"]]),

    Piece([["x", "x", "x"]]),

    Piece([["x", "x", "x", "x"]]),

    Piece([["x", "x", "x", "x", "x"]]),

    Piece([["x"], ["x"]]),

    Piece([["x"], ["x"], ["x"]]),

    Piece([["x"], ["x"], ["x"], ["x"], ["x"]]),

    # L pieces
    Piece([["x"], ["x", "x", "x", "x"]]),

    Piece([[" ", " ", " ", "x"], ["x", "x", "x", "x"]]),

    Piece([["x", "x", "x", "x"], ["x"]]),

    Piece([["x", "x", "x", "x"], [" ", " ", " ", "x"]]),

    Piece([["x", " "], ["x", " "], ["x", " "], ["x", "x"]]),

    Piece([["x", "x"], ["x", " "], ["x", " "], ["x", " "]]),

    Piece([[" ", "x"], [" ", "x"], [" ", "x"], ["x", "x"]]),

    Piece([["x", "x"], [" ", "x"], [" ", "x"], [" ", "x"]]),

    # squares
    Piece([["x", "x"], ["x", "x"]]),

    Piece([["x", "x", "x"], ["x", "x", "x"], ["x", "x", "x"]]),

    # rectangles
    Piece([["x", "x"], ["x", "x"], ["x", "x"]]),

    Piece([["x", "x", "x"], ["x", "x", "x"]]),

    # angle pieces
    Piece([["x", "x"], ["x"]]),

    Piece([["x"], ["x", "x"]]),

    Piece([[" ", "x"], ["x", "x"]]),

    Piece([["x", "x"], [" ", "x"]]),

    # s things
    Piece([["x", "x"], [" ", "x", "x"]]),

    Piece([[" ", "x", "x"], ["x", "x"]]),

    Piece([[" ", "x"], ["x", "x"], ["x", " "]]),

    Piece([["x", " "], ["x", "x"], [" ", "x"]]),

    # middle things
    Piece([["x"], ["x", "x"], ["x"]]),

    Piece([[" ", "x"], ["x", "x"], [" ", "x"]]),

    Piece([[" ", "x", " "], ["x", "x", "x"]]),

    Piece([["x", "x", "x"], [" ", "x", " "]]),

    # all the L's
    Piece([["x", "x", "x"], ["x"], ["x"]]),

    Piece([["x", "x", "x"], [" ", " ", "x"], [" ", " ", "x"]]),

    Piece([[" ", " ", "x"], [" ", " ", "x"], ["x", "x", "x"]]),

    Piece([["x"], ["x"], ["x", "x", "x"]])
]


class Node():
    def __init__(self, parent, total_score, visits, is_player, block=None, blocks=[], seed=None, position=None):
        self.parent = parent
        self.total_score = total_score
        self.visits = visits
        self.is_player = is_player

        # if player, the block to place
        self.block = block

        # if not player, the 3 random blocks
        # otherwise the blocks left to pick
        self.blocks = blocks
        self.seed = seed

        # if player, where to place block
        self.position = position

        self.expanded = False
        self.children = []
        self.UTC = np.inf

        self.CONSTANT = 1.4

    def update_UTC(self):
        if self.visits == 0:
            self.UTC = np.inf
            return
        else:
            self.UTC = self.total_score / self.visits + self.CONSTANT * np.sqrt(
                np.log(self.parent.visits) / self.visits)
