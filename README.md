# quantumfrqi

## Installation and Setup

Setup a new empty environment in python=3.9 ```conda create -n me_env python=3.9```

Install using  ```pip install git+https://github.com/Egupta21/quantumfrqi.git```

## Usage

After installing, create an empty Python file and add the code below:
 ```
from frqi import processimage

processimage('image_name', num_shots=1024*1024, side_dimensions=16)
```

Next, create an empty folder called 'data' and place it in the same folder as the python file created earlier.

image_name = Name of the image without the image type

num_shots = (default 1024*1204) Number of shots you want to perform on prepared state. Higher number leads to higher accuracy but longer run time

side_dimensions = default 16) Side length of the image in pixels. A higher number leads to better-quality image but also a higher run time

## results

If the SSIM is low increase the number of shots. Recommend testing with 16x16 images or 32x32 images for time consideration


