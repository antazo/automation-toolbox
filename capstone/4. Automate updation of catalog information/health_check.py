#!/usr/bin/env python3
'''
Google IT Automation Professional Certificate
CAPSTONE Module 4: Automate updation of catalog information

5. Health check
    Report an error if CPU usage is over 80%
    Report an error if available disk space is lower than 20%
    Report an error if available memory is less than 100MB
    Report an error if the hostname "localhost" cannot be resolved to "127.0.0.1"
'''

import os
import shutil
import sys
import socket
import psutil
import emails

def check_reboot():
    """Returns True if the computer has a pending reboot."""
    return os.path.exists("/run/rebot-required")

def check_disk_full(disk, min_gb, min_percent):
    """ Returns True if there isn't enough space, False otherwise. """
    du = shutil.disk_usage(disk)
    # Calculate the percentage of freespace
    percent_free = 100 * du.free / du.total
    # Calculate how many free gigabytes
    gigabytes_free = du.free / 2**30
    if gigabytes_free < min_gb or percent_free < min_percent:
        return True
    return False

def check_root_full():
    """ Retruns True if the root partition is Full, False otherwise. """
    return check_disk_full(disk="/", min_gb=2, min_percent=20)

def check_cpu_constrained():
    """ Returns True if the cpu is having too much usage, False otherwise. """
    return psutil.cpu_percent(1) > 80

def check_ram_usage():
    """ Returns True if the RAM is having too much usage, False otherwise. """
    return psutil.virtual_memory().available/(1024 * 1024) < 100

def check_localhost():
    """ Returns True if it fails to resolve localhost, False otherwise. """
    try:
        socket.gethostbyname("localhost")
        return False
    except:
        return True

def check_no_network():
    """ Returns True if it fails to resolve Google's URL, False otherwise. """
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True

def main():
    checks=[
        (check_cpu_constrained, "CPU usage is over 80%"),
        (check_root_full, "Available disk space is lower than 20%"),
        (check_ram_usage, "Available memory is less than 100MB"),
        (check_localhost, "Hostname 'localhost' cannot be resolved to '127.0.0.1'"),
        #(check_reboot, "Pending reboot"),
        #(check_no_network, "No working network"),
    ]
    everything_ok = True
    for check, msg in checks:
        if check():
            print(msg)
            everything_ok = False
            
            # Email
            message = emails.generate_email(
                "automation@example.com",
                "student@example.com",
                "Error - " + msg,
                "Please check your system and resolve the issue as soon as possible.",
                )
            print("Sending email...")
            print(message)
            emails.send_email(message)
    if not everything_ok:
        sys.exit(1)
    print("Everything ok.")
    sys.exit(0)

main()
