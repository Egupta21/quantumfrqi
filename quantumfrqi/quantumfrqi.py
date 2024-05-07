from .image_utils import prepare_dimensions, expand_image, is_square, image_width, image_height, remove_padding
from .quantum_functions import hadamard, change, binary, cnri, frqi, make_circ, decode, num_qubit_finder
from .data_management import data_preparation, calculate_mse, calculate_ssim, convert_to_image
from qiskit import Aer, execute
from qiskit.tools.visualization import plot_histogram
from PIL import Image
import numpy as np
import sys, math
import time
import matplotlib.pyplot as plt
import csv
from frqi import processimage

def processimage(image_name, num_shots=1024*1024, side_dimension=16):
    image_path = f"./data/images/{IMAGE_NAME}.png"
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"The image file {IMAGE_NAME}.png does not exist in the specified directory.")
        
    """if(min(og_width))
    if(max(og_wdith, og_height) <= 8 and max(og_wdith, og_height) > 4):
        side_dimension = 8
    elif(max(og_wdith, og_height) <= 4 and max(og_wdith, og_height) > 2):
        side_dimension = 4
    else:
        side_dimension = 2"""
        
    print(f"Processing {image_name} with {num_shots} shots...")
    IMAGE_NAME = image_name
    SIZE = (side_dimension, side_dimension)
    if(min(og_width, og_height) > side_dimension):
        prepare_dimensions(f"./data/images/{IMAGE_NAME}.png", f"./data/images/{IMAGE_NAME}{side_dimension}.png", SIZE)
    IMAGE_NAME = IMAGE_NAME+str(side_dimension)
    image_path = f"./data/images/{IMAGE_NAME}.png"
    image = Image.open(image_path)
    og_width = image_width(image)
    og_height = image_height(image)
    side_len = max(og_height, og_width)
    if side_len < 2:
        raise ValueError("Invalid file size: Image must be over 2x2")
    num_qubit = num_qubit_finder(og_height, og_width)
    print(num_qubit)

    if not is_square(image) or int(np.sqrt((2**num_qubit)/2)) != side_len:
        print("The image is not a square")
        image = expand_image(image, int(np.sqrt((2**num_qubit)/2)))
    image_array = np.array(image)
    plt.imshow(image_array, cmap='gray', vmin=0, vmax=255)
    plt.title(f"{IMAGE_NAME} Original")
    plt.show()

    data_preparation(image, f"./data/sheets/{IMAGE_NAME}.xlsx")

    start_time = time.time()
    qc = make_circ(num_qubit, f"./data/sheets/{IMAGE_NAME}.xlsx")
    make_circ_time = time.time() - start_time

    plt.show()
    print("here")
    qc.measure(list(range(num_qubit)), list(range(num_qubit)))

    backend_sim = Aer.get_backend('qasm_simulator')
    #num_shots = 1024*1024  # Or any other number appropriate for your hardware

    start_time = time.time()
    result = execute(qc, backend_sim, shots=num_shots).result()
    execute_time = time.time() - start_time

    print("PRINTING RESULT COUNT")
    print(result.get_counts(qc))

    print("DISPLAYING IMAGE")
    output_file_path = f"./data/output/decoded_{IMAGE_NAME}.png"
    decode(result.get_counts(qc), num_qubit, output_file_path)

    original_image = np.array(Image.open(image_path).convert('L'))
    decoded_image = np.array(Image.open(output_file_path).convert('L'))

    if original_image.shape != decoded_image.shape:
        decoded_image = remove_padding(original_image, decoded_image)

    mse_value = calculate_mse(original_image, decoded_image)
    print("Mean Squared Error:", mse_value)

    ssim_value = None
    if og_height > 6 and og_width > 6:
        ssim_value = calculate_ssim(original_image, decoded_image)
    print("Structural Similarity Index:", ssim_value)

    with open('./data/logs/execution_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([num_qubit, og_height, og_width,
                         ((2**num_qubit)/2) - (og_height * og_width), make_circ_time,
                         time.time() - start_time, execute_time,
                         make_circ_time + (time.time() - start_time) + execute_time,
                         mse_value, ssim_value, num_shots])
    plot_histogram(result.get_counts(qc), figsize=(20, 7))
    plt.show()

if __name__ == "__main__":
    processimage('bull', 1024*1024, 16)