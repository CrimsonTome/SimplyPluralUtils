# Adapted from https://github.com/CrimsonTome/simply-present

import json
import requests
from pathlib import Path

SIMPLY_PLURAL_BASE_URL = "https://api.apparyllis.com/v1"

# get token from file
def getToken():
    tokenPath = Path("Utils/token.json")
    with tokenPath.open(encoding="utf-8") as tokenFile:
        token = json.load(tokenFile)
        return token

# get fronters from the API
def getFronters():
    # fetch the token
    token = getToken()
    # set up for the request
    payload = {}
    headers = {"Authorization": token["SimplyPluralAPIKey"]}
    print(headers)
    response = requests.get(f"{SIMPLY_PLURAL_BASE_URL}/fronters", headers=headers, data=payload)
    return response.json()

getFronters()