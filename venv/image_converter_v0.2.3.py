import cv2
import numpy as np
import svgwrite
import os

# This version functions nearly perfectly, although angle calculations are off and plygon count is massive.

def png_to_svg(input_file, output_file):
    image = cv2.imread(input_file, cv2.IMREAD_UNCHANGED)
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

    gray_image = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
    _, thresholded_image = cv2.threshold(gray_image, 0, 250, cv2.THRESH_BINARY)
    thresholded_image = thresholded_image.astype(np.uint8)

    ret, labels, stats, centers = cv2.connectedComponentsWithStats(thresholded_image, connectivity=8)
    unique_colors = np.unique(image.reshape(-1, image.shape[2]), axis=0)

    dwg = svgwrite.Drawing(output_file, profile='tiny', size=(image.shape[1], image.shape[0]))

    for color in unique_colors:
        if np.all(color == [255, 255, 255, 0]):
            continue

        color_mask = np.all(image == color, axis=-1).astype(np.uint8) * 255
        color_contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in color_contours:
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx_contour = cv2.approxPolyDP(contour, epsilon, True)
            points = [tuple(float(coord) for coord in point[0]) for point in approx_contour]
            fill_color = svgwrite.utils.rgb(color[0], color[1], color[2])
            fill_opacity = color[3] / 255.0
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
