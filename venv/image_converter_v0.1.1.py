import os
import cv2
import numpy as np
import svgwrite
from sklearn.cluster import KMeans

def png_to_svg(input_file, output_file):
    image = cv2.imread(input_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    kmeans = KMeans(n_clusters=5)
    labels = kmeans.fit_predict(pixel_values)
    centers = kmeans.cluster_centers_

    segmented_image = centers[labels.flatten()]
    segmented_image = segmented_image.reshape(image.shape)

    dwg = svgwrite.Drawing(output_file, profile='tiny', size=(image.shape[1], image.shape[0]))
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))

    for i, centers in enumerate(centers):
        mask = cv2.inRange(segmented_image, centers - 1, centers + 1)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        points = [tuple(float(coord) for coord in point[0]) for point in contour]
        fill_color = svgwrite.utils.rgb(centers[0], centers[1], centers[2])
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