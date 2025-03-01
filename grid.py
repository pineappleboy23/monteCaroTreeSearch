import numpy as np

# Manages a grid of values
class Grid():
    def __init__(self, width=8, height=8, default=0):
        self.width = width
        self.height = height
        self.data = np.array([[default for y in range(height)] for x in range(width)])

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
                    self.data[x + r, y + c] = piece[r, c]


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