import os
import cv2
import numpy as np
import svgwrite

def png_to_svg(input_file, output_file):
    image = cv2.imread(input_file, cv2.IMREAD_UNCHANGED)
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

    unique_colors = np.unique(image.reshape(-1, image.shape[2]), axis=0)

    dwg = svgwrite.Drawing(output_file, profile='tiny', size=(image.shape[1], image.shape[0]))

    for unique_color in unique_colors:
        if unique_color[3] == 0:  # Skip transparent colors
            continue

        color_mask = cv2.inRange(image, unique_color, unique_color)
        contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            points = [tuple(float(coord) for coord in point[0]) for point in contour]
            fill_color = svgwrite.utils.rgb(unique_color[0], unique_color[1], unique_color[2])
            fill_opacity = unique_color[3] / 255.0

            dwg.add(dwg.polygon(points, fill=fill_color, stroke=fill_color, fill_opacity=fill_opacity))

    dwg.save()

input_folder = "venv\Input"
output_folder = "venv\Output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + ".svg")
        png_to_svg(input_file, output_file)
