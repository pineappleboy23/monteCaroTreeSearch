import grid

def place_piece_on_board(board, piece, x, y):
    piece_array = piece.to_array()
    for r in range(3):
        for c in range(3):
            if 0 <= x + r < 8 and 0 <= y + c < 8:  # Ensure we don't go out of bounds
                board[x + r, y + c] = piece_array[r, c]
    return board