#! /usr/bin/env python3
'''
Google IT Automation Professional Certificate
CAPSTONE Module 4: Automate updation of catalog information

3. Uploading the descriptions
'''

import os
import re
import requests

source_path = "/home/student/supplier-data/descriptions/"

for description_file in os.listdir(source_path):
    print("Processing " + source_path + description_file + " ... ")
    if description_file.endswith(".txt"):
        # Traverse over each file and, from the contents
        # of these text files, create a dictionary
        item = {}

        file = open(source_path + description_file, "r")
        content=file.readlines()

        item["name"] = content[0] # name
        # Remove "lbs" and convert weight to integer for the API
        image_weight = re.search(r"([\w]*) lbs", content[1])
        item["weight"] = int(image_weight[1]) # weight (in lbs)
        item["description"] = content[2] # description
        # Include image_name for the API
        image_name = re.search(r"([\w]*).txt", description_file)
        item["image_name"] = image_name[1] + ".jpeg" # image name

        file.close()

    print(item)

    # POST to Django REST API
    headers = {"Content-type": "application/json", "charset": "utf-8"}
    response = requests.post("http://34.148.210.233/fruits/", json=item, headers=headers)
    
    print(str(response.status_code))
    if response.status_code == 201:
        print("Everything is OK")
