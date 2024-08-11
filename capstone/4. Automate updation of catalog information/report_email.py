#!/usr/bin/env python3
'''
Google IT Automation Professional Certificate
CAPSTONE Module 4: Automate updation of catalog information

4. Generate a PDF report and send it through email
    Script to generate a PDF report
'''

import os
from datetime import date
import reports
import emails

source_path = "/home/student/supplier-data/descriptions/"

pdf_path = "/tmp/"
pdf_file = "processed.pdf"

if __name__ == "__main__":
    attachment = pdf_path + pdf_file
    title = "Processed Update on " + str(date.today().strftime("%B %d, %Y")) # Today's date (August 11, 2024)
    paragraph_pdf = ""
    paragraph_email = "\n"

    for description_file in os.listdir(source_path):
        print("Processing " + source_path + description_file + " ... ")
        if description_file.endswith(".txt"):

            file = open(source_path + description_file, "r")
            content=file.readlines()

            paragraph_pdf += "name: " + content[0] + "<br/>" # name
            paragraph_pdf += "weight: " + content[1] + "<br/>" # weight (in lbs)
            paragraph_pdf += "<br/>" # blank line

            paragraph_email += "name: " + content[0] + "\n" # name
            paragraph_email += "weight: " + content[1] + "\n" # weight (in lbs)
            paragraph_email += "\n" # blank line

            file.close()

    # Generate PDF
    print("Generating PDF... " + attachment)
    reports.generate_report(attachment, title, paragraph_pdf)

    # Email
    message = emails.generate_email(
        "automation@example.com",
        "student@example.com",
        "Upload Completed - Online Fruit Store",
        "All fruits are uploaded to our website successfully. A detailed list is attached to this email.",
        attachment
        )
    print("Sending email...")
    print(message)
    emails.send_email(message)
