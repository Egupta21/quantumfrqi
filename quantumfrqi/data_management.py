from .image_utils import expand_image, is_square, image_width, image_height, is_square
import openpyxl
import pandas as pd
from PIL import Image
import numpy as np
from sklearn.metrics import mean_squared_error
from skimage.metrics import structural_similarity as ssim

def data_preparation(image, excel_file_path):
    image = image.convert("L")
    
    height = image_height(image)
    width = image_width(image)

    wb = openpyxl.Workbook()
    ws = wb.active
    for y in range(height):
        for x in range(width):
            # Get pixval
            pixel_value = image.getpixel((x, y))
            ws.cell(row=2, column=y*width+x+1, value=pixel_value)

    # Save the Excel workbook
    wb.save(excel_file_path)
    wb.close()
    print("Excel file created successfully.")
    return(excel_file_path)

def convert_to_image(retrieved_image, output_path):
    if retrieved_image.dtype != np.uint8:
        retrieved_image = retrieved_image.astype(np.uint8)
        
    img = Image.fromarray(retrieved_image, 'L')
    
    img.save(output_path)
    print(f"Image saved to {output_path}")
    
def calculate_mse(original_image, decoded_image):
    #original = np.array(Image.open(original_path).convert('L'))
    #decoded = np.array(Image.open(decoded_path).convert('L'))
    
    mse = mean_squared_error(original_image.flatten(), decoded_image.flatten())
    return mse

def calculate_ssim(original_image, decoded_image):
    #original = np.array(Image.open(original_path).convert('L'))
    #decoded = np.array(Image.open(decoded_path).convert('L'))
    
    ssim_value, ssim_map = ssim(original_image, decoded_image, full=True)
    return ssim_value