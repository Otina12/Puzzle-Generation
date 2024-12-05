import math
import os
import random
import numpy as np
from PIL import Image

def create_puzzle(image_path, squares_in_row = 25):
    img = Image.open(image_path).convert("RGB")
    image_array = np.array(img)

    width, height = img.size
    squares = generate_squares(width, height, squares_in_row)
    m, n = len(squares), len(squares[0])

    for i in range(m):
        for j in range(n):
            if i < m - 1:
                draw_bottom_edge(image_array, squares[i][j])
            if j < n - 1:
                draw_right_edge(image_array, squares[i][j])

    result_img = Image.fromarray(image_array)
    result_img.show()
    
    folder_path = os.path.dirname(image_path)
    output_path = os.path.join(folder_path, f'image_{m*n}pieces.jpg')
    result_img.save(output_path)

    return result_img

def cubic_bezier(p0, p1, p2, p3, t):
    k0 = (-t + 1)**3
    k1 = 3 * t * (-t + 1)**2
    k2 = 3 * t**2 * (-t + 1)
    k3 = t**3
    
    return k0 * np.array(p0) + k1 * np.array(p1) + k2 * np.array(p2) + k3 * np.array(p3)

def draw_bezier_curve(image, p0, p1, p2, p3, points = 500):
    for i in range(points + 1):
        t = i / points
        bezier = cubic_bezier(p0, p1, p2, p3, t)
        y, x = int(round(bezier[0])), int(round(bezier[1]))
        if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
            image[y, x] = (0, 0, 0)

def draw_bottom_edge(image, square, base_offset_ratio = 0.25, curve_relative_size = 0.25):
    left, up, right, bottom = square
    square_width = right - left
    square_height = bottom - up
    
    y_direction = random.choice([-1, 1])
    base_offset = random.uniform(0, base_offset_ratio)
    
    P3 = (bottom + y_direction * curve_relative_size * square_height, (left + right) / 2)  # P3 is common to both left and right parts
    # points for left part
    P0 = (bottom, left)
    P1 = (bottom - y_direction * base_offset * square_height, left + 0.75 * square_width)
    P2 = (bottom + y_direction * curve_relative_size * square_height, left)
    draw_bezier_curve(image, P0, P1, P2, P3)
    
    # points for right part
    P0 = (bottom, right)
    P1 = (bottom - y_direction * base_offset * square_height, right - 0.75 * square_width)
    P2 = (bottom + y_direction * curve_relative_size * square_height, right)
    draw_bezier_curve(image, P0, P1, P2, P3)
    
def draw_right_edge(image, square, base_offset_ratio = 0.25, curve_size = 0.3):
    left, up, right, bottom = square
    square_width = right - left
    square_height = bottom - up
    
    x_direction = random.choice([-1, 1])
    base_offset = random.uniform(0, base_offset_ratio)
    
    P3 = ((bottom + up) / 2, right + x_direction * curve_size * square_width) # P3 is common to both left and right parts
    # points for upper part
    P0 = (up, right)
    P1 = (up + 0.75 * square_height, right - x_direction * base_offset * square_width)
    P2 = (up, right + x_direction * curve_size * square_width)
    draw_bezier_curve(image, P0, P1, P2, P3)
    
    # points for lower part
    P0 = (bottom, right)
    P1 = (bottom - 0.75 * square_height, right - x_direction * base_offset * square_width)
    P2 = (bottom, right + x_direction * curve_size * square_width)
    draw_bezier_curve(image, P0, P1, P2, P3)

def generate_squares(w, h, squares_in_row):
    ratio = w / h
    
    rows = squares_in_row
    cols = math.floor(rows * ratio)
    
    print(rows)
    print(cols)
    square_width = w / cols
    square_height = h / rows
    
    squares = []
    
    for row in range(rows):
        row_squares = []
        for col in range(cols):
            left = col * square_width
            upper = row * square_height
            right = (col + 1) * square_width
            lower = (row + 1) * square_height
            
            if col == cols - 1:
                right = min(right, w)
            if row == rows - 1:
                lower = min(lower, h)
            
            row_squares.append((left, upper, right, lower))
        squares.append(row_squares)

    return squares

image_path = 'images/image.png'
squares_in_row = 10 # for larger values, it's better to decrease 'points' default parameter of method draw_bezier_curve
create_puzzle(image_path, squares_in_row) 