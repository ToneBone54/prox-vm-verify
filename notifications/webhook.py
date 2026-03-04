# Note for development:
# If testing this script directly, do not use the "Run script" button in VSCode. 
# Something is wrong between the script execution path and the auth package import

# Workaround: Run as a Python module in the terminal. This makes it behave.
# python -m notifications.webhook

import requests as req
from prox_auth import pve
import json

# Any webhook endpoint. For my testing, I'm using a Home Assistant webhook 
url = "<webhook endpoint>"

version = pve.version.get()
headers = {
    "Content-Type": "application/json",
}
payload = {
    "title": "Test post",
    "message": "Version: %s" % version
}

req.post(url, headers=headers, json=payload)