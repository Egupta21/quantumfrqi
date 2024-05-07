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
    print("Original Image:")
    print(original_image)
    print("Decoded Image:")
    print(decoded_image)

    original_height, original_width = original_image.shape

    col_sum = np.sum(decoded_image, axis=0)
    valid_cols = col_sum > 0
    cropped_image = decoded_image[:, valid_cols]

    row_sum = np.sum(cropped_image, axis=1)
    valid_rows = row_sum > 0
    cropped_image = cropped_image[valid_rows, :]

    if cropped_image.shape[0] > original_height:
        cropped_image = cropped_image[:original_height, :]
    if cropped_image.shape[1] > original_width:
        cropped_image = cropped_image[:, :original_width]

    print(cropped_image)
    return cropped_image

def prepare_dimensions(input_image_path, output_image_path, new_size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(new_size)
    bw_image = resized_image.convert("L") 
    bw_image.save(output_image_path)