from typing import List, Tuple

# (left, up, right, bottom)
Square = Tuple[int, int, int, int]

def generate_squares(width: int, height: int, squares_in_row: int):
    n = squares_in_row
    m = round(height / (width / n))
    cell_w = width // n
    cell_h = height // m
    squares = []
    
    for i in range(m):
        row = []
        for j in range(n):
            left = j * cell_w
            up = i * cell_h
            right = width if j == n - 1 else (j + 1) * cell_w
            bottom = height if i == m - 1 else (i + 1) * cell_h
            row.append((left, up, right, bottom))
        squares.append(row)

    return squares
