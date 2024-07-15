#!/usr/bin/env python3
"""
For now, this code retrieves the list of characters
from the first Dragon Ball, through a REST API in
the following endpoint:

https://apidragonball.vercel.app/dragonball

Kudos to Juan Pablo! https://juanppdev.vercel.app/
"""


import requests

base_URL = "https://apidragonball.vercel.app"

response = requests.get(base_URL + "/dragonball")

if response.status_code == 200:
    print(response.json())