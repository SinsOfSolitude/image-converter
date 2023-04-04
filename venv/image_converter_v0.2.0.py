import os
import cairosvg
import cv2

def png_to_svg(input_file, output_file):
    # Read the image
    image = cv2.imread(input_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Save the image as a temporary PNG file
    temp_png_file = "temp.png"
    cv2.imwrite(temp_png_file, image)

    # Convert the temporary PNG file to an SVG file
    cairosvg.png2svg(url=temp_png_file, write_to=output_file)

    # Remove the temporary PNG file
    os.remove(temp_png_file)

input_folder = "venv\Input"
output_folder = "venv\Output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + ".svg")
        png_to_svg(input_file, output_file)
