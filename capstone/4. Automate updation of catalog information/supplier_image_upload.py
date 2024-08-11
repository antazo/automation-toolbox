#!/usr/bin/env python3
'''
Google IT Automation Professional Certificate
CAPSTONE Module 4: Automate updation of catalog information

2. Uploading images to web server
'''

import os
import requests

input_images= "/home/student//supplier-data/images/"

url = "http://localhost/upload/"

if os.path.exists(input_images):
    for image in os.listdir(input_images):
        if image.endswith(".jpeg"):
            # Prints only text file present in My Folder
            #print(image)

            print("Uploading " + input_images + image + " ... ")
            with open(input_images + image, 'rb') as opened:
                r = requests.post(url, files={'file': opened})
    print("Upload successful!")
else:
    print("Missing input path " + input_images)