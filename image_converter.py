import os
import potrace
import numpy as np
from PIL import Image

def png_to_svg(input_file, output_file):
    image = Image.open(input_file).convert("L")
    image = image.point(lambda x: 0 if x < 128 else 255, "1")
    bitmap = potrace.Bitmap(np.array(image))
    path = list(bitmap.to_path())

    with open(output_file, "w") as svg:
        svg.write(f'<svg width="{image.width}" height="{image.height}" viewBox="0 0 {image.width} {image.height}" xmlns="http://www.w3.org/2000/svg">\n')
        for p in path:
            d = " ".join(f"{cmd}{x},{y}" for cmd, x, y in p)
            svg.write(f'<path d="{d}" fill="black"/>\n')
        svg.write('</svg>\n')

input_folder = "Input"
output_folder = "Output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + ".svg")
        png_to_svg(input_file, output_file)
