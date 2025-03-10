# Adapted from https://github.com/CrimsonTome/simply-present

import json
import requests
from pathlib import Path

SIMPLY_PLURAL_BASE_URL = "https://api.apparyllis.com/v1"

# return the token from the user's token file
def getToken(userPath):
    tokenPath = Path(userPath)
    with tokenPath.open(encoding="utf-8") as tokenFile:
        token = json.load(tokenFile)
        return token


# returns a list of all fronter IDs from the /fronters endpoint
# https://docs.apparyllis.com/docs/api/get-current-fronters-self
def getAllFronterID(token):
    response = requests.get(f"{SIMPLY_PLURAL_BASE_URL}/fronters", headers=headers, data=payload, timeout=10)
    fronters = json.loads(response.text)
    # print(data)
    return fronters

# returns a list of fronter IDs from the fronters list
def getFronterIDList(fronters):
    fronter_id_list = [
        item["content"]["member"]
        for item in fronters
        if not item["content"].get("custom", False)
    ]
    return fronter_id_list

# returns a list of custom fronter IDs from the fronters list 
def getCustomFronterIDList(fronters):
    custom_fronter_id_list = [
        item["content"]["member"]
        for item in fronters
        if item["content"].get("custom", False)
    ]
    return custom_fronter_id_list

# returns the stripped system ID using the first fronter
# you can also use the /me endpoint to get the system ID with some more filtering
def getUID(fronters):
    return fronters[0]["content"]["uid"]


def getAllFronterList(fronterList, UID):
    fronterListConc = []
    for i in range(len(fronterList)):
        response = requests.get(f"{SIMPLY_PLURAL_BASE_URL}/member/{UID}/{fronterList[i]}", headers=headers, data=payload, timeout=10)
        content = json.loads(response.text)
        name = content["content"]["name"]
        avatar = content["content"]["avatarUrl"]
        fronterListConc.append((name, avatar))
    return fronterListConc


# fix headers and payload

# make the full fronters list


# would be in other files
token = getToken("Utils/token.json")
payload= {}
headers = {"Authorization": token["SimplyPluralAPIKey"]}

fronters = getAllFronterID(token)

fronterList = getFronterIDList(fronters)
customFronterList = getCustomFronterIDList(fronters)
print(fronterList)
# print(customFronterList)

UID = getUID(fronters)

allFronterList = getAllFronterList(fronterList, UID)
print(allFronterList)