# quantumfrqi

## Installation and Setup

Setup a new empty environment

Install using  ```python pip install git+https://github.com/Egupta21/quantumfrqi.git```

## Usage

After installing, use as follows:
 ```python
from frqi import processimage

processimage('image_name', num_shots, side_dimensions)
```
image_name = Name of the image without the image type

num_shots = (default 1024*1204) Number of shots you want to perform on prepared state. Higher number leads to higher accuracy but longer run time

side_dimensions = Side length of the image in pixels. A higher number leads to better-quality image but also a higher run time


