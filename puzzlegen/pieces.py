import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from .grid import generate_squares
from .puzzle import create_puzzle
from .shapes import _bezier, draw_bottom_edge, draw_right_edge

def _draw_edges_mask(width, height, squares, seed, thicken=3):
    random.seed(seed)
    mask = Image.new("L", (width, height), 0)
    dr = ImageDraw.Draw(mask)

    m, n = len(squares), len(squares[0])

    for i in range(m):
        for j in range(n):
            if i < m - 1:
                draw_bottom_edge(dr, squares[i][j], width = 3, fill = 255)
            if j < n - 1:
                draw_right_edge(dr, squares[i][j], width = 3, fill = 255)

    dr.rectangle([(0, 0), (width - 1, height - 1)], outline = 255, width = 1)

    if thicken and thicken > 1:
        size = thicken if thicken % 2 == 1 else thicken + 1
        mask = mask.filter(ImageFilter.MaxFilter(size = size))

    return mask


def _flood_region(obstacles_bool, seed_xy):
    h, w = obstacles_bool.shape
    sx, sy = seed_xy

    if not (0 <= sx < w and 0 <= sy < h):
        return np.zeros((h, w), dtype = bool)
    if obstacles_bool[sy, sx]:
        return np.zeros((h, w), dtype = bool)

    seen = np.zeros((h, w), dtype=  bool)
    st = [(sx, sy)]
    seen[sy, sx] = True
    while st:
        x, y = st.pop()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h:
                if not seen[ny, nx] and not obstacles_bool[ny, nx]:
                    seen[ny, nx] = True
                    st.append((nx, ny))
                    
    return seen

def save_pieces(image_path: str, squares_in_row: int = 25, edge_thicken: int = 3, seed: int = None, output_dir: str = None):
    if seed is None:
        seed = random.randrange(1 << 30)

    random.seed(seed)

    src_rgba = Image.open(image_path).convert("RGBA")
    w, h = src_rgba.size
    squares = generate_squares(w, h, squares_in_row)
    mask_img = _draw_edges_mask(w, h, squares, seed = seed, thicken = edge_thicken)
    obstacles = np.array(mask_img, dtype=np.uint8) > 0

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    total_pieces = len(squares) * len(squares[0])

    if output_dir:
        output_dir = os.path.join(output_dir, f"{base_name}{total_pieces}pcs_pieces")
    else:
        output_dir = os.path.join(os.path.dirname(image_path), f"{base_name}{total_pieces}pcs_pieces")
        
    os.makedirs(output_dir, exist_ok = True)

    rows, cols = len(squares), len(squares[0])
    for r in range(rows):
        for c in range(cols):
            left, up, right, bottom = squares[r][c]
            cx = int((left + right) / 2)
            cy = int((up + bottom) / 2)

            reg = _flood_region(obstacles, (cx, cy))
            if not reg.any():
                for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (2,0), (-2,0), (0,2), (0,-2)]:
                    reg = _flood_region(obstacles, (cx + dx, cy + dy))
                    if reg.any():
                        break

            alpha = Image.fromarray((reg * 255).astype("uint8"), mode = "L")
            piece = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            piece.paste(src_rgba, (0, 0), mask = alpha)

            bbox = alpha.getbbox()
            if bbox:
                piece = piece.crop(bbox)

            out_path = os.path.join(output_dir, f"{base_name}_piece-{r}_{c}.png")
            piece.save(out_path)

    return output_dir
