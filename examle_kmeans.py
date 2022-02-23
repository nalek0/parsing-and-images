from PIL import ImageDraw

from kmeans import *

K = 3

if __name__ == "__main__":
    original = Art("images/original.jpg")
    small = original.get_resized_art((128, 128), "images/input.jpg")
    result_colors = Art.kmeans(small.get_pixels(), K)

    image = Image.open("images/output.jpg")
    draw = ImageDraw.Draw(image)
    for x in range(image.width):
        for y in range(image.height):
            col = result_colors[K * x // image.width]
            draw.point((x, y), (col.red, col.green, col.blue))
    image.save("images/output.jpg", "JPEG")
    del draw
