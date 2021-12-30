from PIL import Image
from collections import Counter

img = Image.open("image7")
img = img.convert("RGB")

width, height = img.size

all_pixels = []

for x in range(0, width):
    for y in range(0, height):
        r, g, b = img.getpixel((x, y))
        all_pixels.append([r, g, b])

converted_pixels = map(tuple, all_pixels)

count = dict(Counter(converted_pixels))
print(count)

