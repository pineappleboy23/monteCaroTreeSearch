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

    def piece_fits(self, piece, x, y):
        piece_board = np.zeros((8, 8))
        for r in range(3):
            for c in range(3):
                if 0 <= x + r < 8 and 0 <= y + c < 8:  # Ensure we don't go out of bounds
                    piece_board[x + r, y + c] = piece[r, c]


        return np.max(piece_board + self.data) < 2

    def add_piece(self, piece, x, y):
        for r in range(3):
            for c in range(3):
                if 0 <= x + r < 8 and 0 <= y + c < 8:  # Ensure we don't go out of bounds
                    self.data[x + r, y + c] += piece[r, c]

        # add up score and remove filled rows and cols
        self.clear_lines()

    def generate_3_pieces(self):
        p = []
        if len(self.pieces) == 0:
            for i in range(3):
                p.append(Piece(random.choice(pieces)).arr)
        return p

    def possible_moves(self, piece):
        moves = []
        for x in range(6):
            for y in range(6):
                if self.piece_fits(piece, x, y):
                    moves.append((x, y))
        return moves

    # returns (game_ended, score)
    def random_move(self):
        self.score += 1
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
        self.shape = shape
        self.arr = self.to_array()


    def __str__(self):
        return self.render()

    def to_array(self):
        # Get the shape dimensions
        rows = len(self.shape)
        cols = max(len(row) for row in self.shape)

        # Initialize a 3x3 array with zeros
        array = np.zeros((3, 3), dtype=int)

        # Fill in the "x" values with 1s
        for r, row in enumerate(self.shape):
            for c, char in enumerate(row):
                if r < 3 and c < 3:
                    array[r, c] = 1 if char == "x" else 0

        return array


    def render(self):
        res = []

        for row in self.shape:
            res.append("".join(row)+"\n")

        return "".join(res)


pieces = [Piece([["x"]]),
          Piece([["x", "x"]]),
          Piece([["x", "x", "x"]]),
          Piece([["x", "x", "x", "x"]]),
          Piece([["x"],["x"]]),
          Piece([["x"], ["x"], ["x"]]),
          Piece([["x"], ["x"], ["x"], ["x"]]),
          Piece([["x", "x"], ["x", "x"]]),
          Piece([["x", "x"], ["x"]]),
          Piece([["x"], ["x", "x"]]),
          Piece([[" ", "x"], ["x", "x"]]),
          Piece([["x", "x"], [" ", "x"]]),
          Piece([["x", "x", "x"], ["x"], ["x"]]),
          Piece([["x", "x", "x"], [" ", " ", "x"], [" ", " ", "x"]]),
          Piece([[" ", " ", "x"], [" ", " ", "x"], ["x", "x", "x"]]),
          Piece([["x"], ["x"], ["x", "x", "x"]])
         ]


class Node():
    def __init__(self, parent, total_score, visits, is_player, block=None, blocks=None, seed=None):
        self.parent = parent
        self.total_score = total_score
        self.visits = visits
        self.is_player = is_player
        self.block = block
        self.blocks = blocks
        self.seed = seed

        self.expanded = False
        self.children = []
        self.UTC = np.inf

        self.CONSTANT = 1.4

        self.simulations = 0


    def update_UTC(self):
        if self.visits == 0:
            self.UTC = np.inf
            return
        else:
            self.UTC = self.total_score/self.visits + self.CONSTANT * np.sqrt(np.log(self.parent.simulations)/self.visits)

