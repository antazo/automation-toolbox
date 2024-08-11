#!/usr/bin/env python3
'''
Google IT Automation Professional Certificate
CAPSTONE Module 4: Automate updation of catalog information

1. Working with supplier images
    Size: Change image resolution from 3000x2000 to 600x400 pixel
    Format: Change image format from .TIFF to .JPEG
'''

import os
import re
from PIL import Image

input_images= "/home/student/supplier-data/images/"
output_images= "/home/student/supplier-data/images/"


if os.path.exists(input_images):
    if os.path.exists(output_images):
        for image in os.listdir(input_images):
            if image.endswith(".tiff"):
                # Prints only text file present in My Folder
                #print(image)
                print("Processing " + input_images + image + " ... ")
                im = Image.open(input_images + image)
                if im.mode != 'RGB':
                    im = im.convert('RGB')
                image_name = re.search(r"([\w]*).tiff", image)
                im.resize((600,400)).save(output_images + image_name[1] + ".jpeg")
    else:
        print("Missing output path " + output_images)
else:
    print("Missing input path " + input_images)