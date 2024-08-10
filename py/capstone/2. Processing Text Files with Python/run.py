#! /usr/bin/env python3

# Google IT Automation Professional Certificate
# CAPSTONE Module 2: Processing Text Files with Python
# Dictionaries and Uploading to Running Web Service

import os
import requests

source_path = "/data/feedback/"

for feedback_file in os.listdir(source_path):
    print("Processing " + source_path + feedback_file)
    if feedback_file.endswith(".txt"):
        # Traverse over each file and, from the contents
        # of these text files, create a dictionary
        feedback = {}

        file = open(source_path + feedback_file, "r")
        content=file.readlines()

        feedback["title"] = content[0] # title
        feedback["name"] = content[1] # name
        feedback["date"] = content[2] # date
        feedback["feedback"] = content[3] # feedback

        file.close()

    print(feedback)

    # POST to Django REST API
    headers = {"Content-type": "application/json", "charset": "utf-8"}
    response = requests.post("http://35.230.48.201/feedback/", json=feedback, headers=headers)
    
    print(str(response.status_code))
    if response.status_code == 201:
        print("Everything is OK")
