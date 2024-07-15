#!/usr/bin/env python3

import requests

base_URL = "https://apidragonball.vercel.app"

response = requests.get(base_URL + "/dragonball")

if response.status_code == 200:
    print(response.json())