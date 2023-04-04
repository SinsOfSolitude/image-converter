import cv2
import numpy as np
import svgwrite
import os

# This version functions nearly perfectly, although polygon count is massive.

def png_to_svg(input_file, output_file):
    image = cv2.imread(input_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, thresholded_image = cv2.threshold(gray_image, 0, 250, cv2.THRESH_BINARY)
    thresholded_image = thresholded_image.astype(np.uint8)

    ret, labels, stats, centers = cv2.connectedComponentsWithStats(thresholded_image, connectivity=8)
    unique_colors = np.unique(image.reshape(-1, image.shape[2]), axis=0)

    dwg = svgwrite.Drawing(output_file, profile='tiny', size=(image.shape[1], image.shape[0]))

    for color in unique_colors:
        if np.all(color == [255, 255, 255]):
            continue

        color_mask = np.all(image == color, axis=-1).astype(np.uint8) * 255
        color_contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in color_contours:
            points = [tuple(float(coord) for coord in point[0]) for point in contour]
            fill_color = svgwrite.utils.rgb(color[0], color[1], color[2])
            dwg.add(dwg.polygon(points, fill=fill_color, stroke=fill_color))

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
