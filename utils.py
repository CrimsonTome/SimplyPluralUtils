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
def getAllFronterID():
    response = requests.get(f"{SIMPLY_PLURAL_BASE_URL}/fronters", headers=headers, data=payload, timeout=10)
    fronters = json.loads(response.text)
    return fronters

# returns a list of fronter IDs from the fronters list
def craftFronterIDList(fronters):
    fronter_id_list = [
        item["content"]["member"]
        for item in fronters
        if not item["content"].get("custom", False)
    ]
    return fronter_id_list

# returns a list of custom fronter IDs from the fronters list 
def craftCustomFronterIDList(fronters):
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

# returns a list of fronter names and avatar URLs from both the fronter list and custom fronter list
def getAllFronterInfo(fronterList, customFronterList, UID):
    fronterListConc = []
    for i in range(len(fronterList)):
        response = requests.get(f"{SIMPLY_PLURAL_BASE_URL}/member/{UID}/{fronterList[i]}", headers=headers, data=payload, timeout=10)
        content = json.loads(response.text)
        name = content["content"]["name"]
        avatar = content["content"]["avatarUrl"]
        fronterListConc.append((name, avatar))
    for i in range(len(customFronterList)):
        response = requests.get(f"{SIMPLY_PLURAL_BASE_URL}/customfront/{UID}/{customFronterList[i]}", headers=headers, data=payload, timeout=10)
        content = json.loads(response.text)
        name = content["content"]["name"]
        avatar = content["content"]["avatarUrl"]
        fronterListConc.append((name,avatar))
    return fronterListConc

# here and below would be in other files
# replace with your own path, start at the root of the project
token = getToken("token.json")

# set up for making requests
payload= {}
headers = {"Authorization": token["SimplyPluralAPIKey"]}

fronters = getAllFronterID()

fronterList = craftFronterIDList(fronters)
customFronterList = craftCustomFronterIDList(fronters)

UID = getUID(fronters)

allFronterList = getAllFronterInfo(fronterList,customFronterList, UID)
print(allFronterList)
