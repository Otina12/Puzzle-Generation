import os
import random
from PIL import Image, ImageDraw
from .grid import generate_squares
from .shapes import draw_bottom_edge, draw_right_edge

def create_puzzle(image_path: str, squares_in_row: int = 25, output_dir: str = None):
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    squares = generate_squares(w, h, squares_in_row)

    m, n = len(squares), len(squares[0])
    edges = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(edges)

    for i in range(m):
        for j in range(n):
            if i < m - 1:
                draw_bottom_edge(dr, squares[i][j])
            if j < n - 1:
                draw_right_edge(dr, squares[i][j])

    out = Image.new("RGBA", (w, h))
    out.paste(img, (0, 0))
    out.alpha_composite(edges)

    total_pieces = m * n

    if output_dir is None:
        output_dir = os.path.dirname(image_path)
    os.makedirs(output_dir, exist_ok = True)

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    save_name = f"{base_name}_{total_pieces}pieces.jpg"
    save_path = os.path.join(output_dir, save_name)

    out_rgb = out.convert("RGB")
    out_rgb.save(save_path, "JPEG", quality = 95)

    return save_path
