#!/usr/bin/env python3

from email.message import EmailMessage

message = EmailMessage()
sender = "me@example.com"
recipient = "you@example.com"

message['From'] = sender
message['To'] = recipient
message['Subject'] = 'Greetings from {} to {}!'.format(sender, recipient)

body = """Hey there!

I'm learning to send emails using Python!"""
message.set_content(body)

# Attachment
import os.path
attachment_path = "/tmp/example.png"
attachment_filename = os.path.basename(attachment_path)
import mimetypes
mime_type, _ = mimetypes.guess_type(attachment_path) # image/png
mime_type, mime_subtype = mime_type.split('/', 1) # mime_type = image, mime_subtype = png

# Add it to message
with open(attachment_path, 'rb') as ap:
     message.add_attachment(ap.read(),
                            maintype=mime_type,
                            subtype=mime_subtype,
                            filename=os.path.basename(attachment_path))

# Send it!

import smtplib
#mail_server = smtplib.SMTP('localhost')
mail_server = smtplib.SMTP_SSL('smtp.example.com')
mail_server.set_debuglevel(1)

# Authenticate to the SMTP server
import getpass
mail_pass = getpass.getpass('Password? ')

try:
    mail_server.login(sender, mail_pass)
    mail_server.send_message(message)
except smtplib.SMTPAuthenticationError as smtp_error:
    print("Error authenticating: " + smtp_error)
finally:
    mail_server.quit()

'''
SMTP status codes

   235 2.7.0  Authentication Succeeded
   432 4.7.12  A password transition is needed
   454 4.7.0  Temporary authentication failure
   534 5.7.9  Authentication mechanism is too weak
   535 5.7.8  Authentication credentials invalid
   500 5.5.6  Authentication Exchange line is too long
   530 5.7.0  Authentication required
   538 5.7.11  Encryption required for requested authentication
               mechanism
   The following 3 Enhanced Status Codes were defined above:
       5.7.8 Authentication credentials invalid
       5.7.9 Authentication mechanism is too weak
       5.7.11 Encryption required for requested authentication mechanism
   X.5.6     Authentication Exchange line is too long
'''