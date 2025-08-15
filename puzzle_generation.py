from puzzlegen import generate_squares, create_puzzle, save_pieces

__all__ = ["generate_squares", "create_puzzle", "save_pieces"]

# save whole puzzle image
output_path = create_puzzle("images/image.png", squares_in_row = 10, output_dir = "images")
print(f"Puzzle saved to: {output_path}")

print()

# save each puzzle piece image
output_path = save_pieces("images/image.png", squares_in_row = 5, seed = 123, output_dir = "images")
print(output_path)