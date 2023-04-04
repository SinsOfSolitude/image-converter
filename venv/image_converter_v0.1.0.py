import os
import cv2
import numpy as np
import svgwrite

def png_to_svg(input_file, output_file):
    image = cv2.imread(input_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    dwg = svgwrite.Drawing(output_file, profile='tiny', size=(image.shape[1], image.shape[0]))
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))

    for contour in contours:
        mask = np.zeros(gray_image.shape, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)
        color = cv2.mean(image, mask=mask)

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
