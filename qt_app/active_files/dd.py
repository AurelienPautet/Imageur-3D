from PIL import Image, ImageDraw

# Define the size of the chessboard
square_size = 100  # Length of each square
width = 12 * square_size  # 10 squares wide
height = 8 * square_size  # 8 squares tall

# Create a new image with a white background
chessboard = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(chessboard)

# Draw the chessboard pattern
for row in range(8):  # 8 rows
    for col in range(12):  # 10 columns
        if (row + col) % 2 == 0:  # Black squares
            x0 = col * square_size
            y0 = row * square_size
            x1 = x0 + square_size
            y1 = y0 + square_size
            draw.rectangle([x0, y0, x1, y1], fill="black")
            # Draw a thin circle centered in the middle of the chessboard
center_x = width // 2
center_y = height // 2
radius = square_size // 2
draw.ellipse(
    [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
    outline="red",
    width=1
)
# Save the image
chessboard.save("chessboard.png")