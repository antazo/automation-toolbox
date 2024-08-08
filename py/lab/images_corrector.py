#!/usr/bin/env python3

import os
from PIL import Image

input_images= "/home/student/images/"
output_images= "/opt/icons/"

if os.path.exists(input_images):
    if os.path.exists(output_images):
        for image in os.listdir(input_images):
            if image.endswith("48dp"):
                # Prints only text file present in My Folder
                #print(image)

                # Rotate the image 90   clockwise
                # Resize the image from 192x192 to 128x128
                # Save the image to a new folder in .jpeg format

                print("Processing " + input_images + image + "...")
                im = Image.open(input_images + image)
                if im.mode != 'RGB':
                    im = im.convert('RGB')
                im.rotate(90).resize((128,128)).save(output_images + image + ".jpeg")
    else:
        print("Missing output path " + output_images)
else:
    print("Missing input path " + input_images)