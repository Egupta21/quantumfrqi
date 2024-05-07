from PIL import Image
import numpy as np

def image_height(image):
    width, height = image.size
    return height

def image_width(image):
    width, height = image.size
    return width

def is_square(image):
    width, height = image.size
    return height == width

def expand_image(image, side_length):
    width, height = image.size
    square_image = Image.new("RGB", (side_length, side_length), (0, 0, 0))

    grayscale_image = image.convert("L")

    paste_x = 0
    paste_y = 0
    if width <= side_length and height <= side_length:
        paste_x = 0
        paste_y = 0
    square_image.paste(grayscale_image, (paste_x, paste_y))

    return square_image

def remove_padding(original_image, decoded_image):
    new_image = np.zeros_like(original_image)
    original_height, original_width = original_image.shape
    decoded_height, decoded_width = decoded_image.shape

    for i in range(original_height):
        for j in range(original_width):
            if i <= decoded_height and j <= decoded_width:
                new_image[i, j] = decoded_image[i, j]

    print("Original Image:")
    print(original_image)
    print("Decoded Image:")
    print(decoded_image)
    print("New Image with Decoded Values:")
    print(new_image)

    return new_image

def prepare_dimensions(input_image_path, output_image_path, new_size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(new_size)
    bw_image = resized_image.convert("L") 
    bw_image.save(output_image_path)