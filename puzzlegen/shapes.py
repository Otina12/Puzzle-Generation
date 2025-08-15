# puzzlegen/shapes.py
import random
from PIL import ImageDraw
from typing import Tuple, List

Point = Tuple[float, float]

def _bezier(p0: Point, p1: Point, p2: Point, p3: Point, steps: int = 500) -> List[Point]:
    pts: List[Point] = []

    for i in range(steps + 1):
        t = i / steps
        k0 = (1 - t) ** 3
        k1 = 3 * t * (1 - t) ** 2
        k2 = 3 * t * t * (1 - t)
        k3 = t ** 3
        x = k0 * p0[0] + k1 * p1[0] + k2 * p2[0] + k3 * p3[0]
        y = k0 * p0[1] + k1 * p1[1] + k2 * p2[1] + k3 * p3[1]
        pts.append((x, y))

    return pts

def draw_bottom_edge(draw: ImageDraw.ImageDraw, square, base_offset_ratio = 0.25, curve_relative_size = 0.25, width: int = 2, fill = (0, 0, 0)):
    left, up, right, bottom = square
    square_w = right - left
    square_h = bottom - up
    ydir = random.choice([-1, 1])
    base = random.uniform(0, base_offset_ratio)
    P3 = ((left + right) / 2, bottom + ydir * curve_relative_size * square_h)

    # left half
    P0 = (left, bottom)
    P1 = (left + 0.75 * square_w, bottom - ydir * base * square_h)
    P2 = (left, bottom + ydir * curve_relative_size * square_h)
    pts = _bezier(P0, P1, P2, P3)
    draw.line(pts, fill = fill, width = width)

    # right half
    P0 = (right, bottom)
    P1 = (right - 0.75 * square_w, bottom - ydir * base * square_h)
    P2 = (right, bottom + ydir * curve_relative_size * square_h)
    pts = _bezier(P0, P1, P2, P3)
    draw.line(pts, fill = fill, width = width)

def draw_right_edge(draw: ImageDraw.ImageDraw, square, base_offset_ratio = 0.25, curve_size = 0.30, width: int = 2, fill = (0, 0, 0)):
    left, up, right, bottom = square
    square_w = right - left
    square_h = bottom - up
    xdir = random.choice([-1, 1])
    base = random.uniform(0, base_offset_ratio)
    P3 = (right + xdir * curve_size * square_w, (up + bottom) / 2)

    # upper half
    P0 = (right, up)
    P1 = (right - xdir * base * square_w, up + 0.75 * square_h)
    P2 = (right + xdir * curve_size * square_w, up)
    pts = _bezier(P0, P1, P2, P3)
    draw.line(pts, fill = fill, width = width)

    # lower half
    P0 = (right, bottom)
    P1 = (right - xdir * base * square_w, bottom - 0.75 * square_h)
    P2 = (right + xdir * curve_size * square_w, bottom)
    pts = _bezier(P0, P1, P2, P3)
    draw.line(pts, fill = fill, width = width)
