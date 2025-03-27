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
    response = requests.get(
        f"{SIMPLY_PLURAL_BASE_URL}/fronters", headers=headers, data=payload, timeout=10
    )
    fronters = response.json()
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

def getNonCustomFronters(fronterList, UID):
    fronterListConc = []
    for i in range(len(fronterList)):
        response = requests.get(
            f"{SIMPLY_PLURAL_BASE_URL}/member/{UID}/{fronterList[i]}",
            headers=headers,
            data=payload,
            timeout=10,
        )
        fronters = response.json()
        content = fronters["content"]
        # check if the contents of pronouns after stripping whitespace is not empty
        # do this to filter out test or uncomplete members
        if content["pronouns"].strip():
            fronterListConc.append(
                (
                    content["name"],
                    content["avatarUrl"],
                    content["pronouns"],
                    content["desc"],
            )
        )
    return fronterListConc

def getCustomFronters(customFronterList, UID):
    customFronterListConc = []
    for i in range(len(customFronterList)):
        response = requests.get(
            f"{SIMPLY_PLURAL_BASE_URL}/customfront/{UID}/{customFronterList[i]}",
            headers=headers,
            data=payload,
            timeout=10,
        )
        customFronters = response.json()
        
        content = customFronters["content"]
        customFronterListConc.append(
            (
                content["name"],
                content["avatarUrl"],
                content["desc"],
            )
        )


# returns a list of fronter names and avatar URLs from both the fronter list and custom fronter list
def getAllFronterInfo(fronterList, customFronterList, UID):
    fronterListConc = []
    for i in range(len(fronterList)):
        response = requests.get(
            f"{SIMPLY_PLURAL_BASE_URL}/member/{UID}/{fronterList[i]}",
            headers=headers,
            data=payload,
            timeout=10,
        )
        fronters = response.json()
        for member in fronters:
            content = member["content"]
            # check if the contents of pronouns after stripping whitespace is not empty
            # do this to filter out test or uncomplete members
            if content["pronouns"].strip():
                fronterListConc.append(
                    (
                        content["name"],
                        content["avatarUrl"],
                        content["pronouns"],
                        content["desc"],
                    )
            )
    for i in range(len(customFronterList)):
        response = requests.get(
            f"{SIMPLY_PLURAL_BASE_URL}/customfront/{UID}/{customFronterList[i]}",
            headers=headers,
            data=payload,
            timeout=10,
        )
        content = response.json()
        name = content["content"]["name"]
        avatar = content["content"]["avatarUrl"]
        fronterListConc.append((name, avatar))
    return fronterListConc


def getChainNonCustomFronterInfo():
    fronterIDs = getAllFronterID()
    fronterIDList = craftFronterIDList(fronterIDs)
    UID = getMe()
    fronterList = getNonCustomFronters(fronterIDList, UID)
    return fronterList

# TODO: this is currently broken. need to fix later
def getChainCustomFronterInfo():
    customFronterIDs = getAllFronterID()
    customFronterIDList = craftCustomFronterIDList(customFronterIDs)
    UID = getMe()
    customFronterList = getCustomFronters(customFronterIDList, UID)
    return customFronterList

# returns a list containing fronter information for those that match the query
# looks for an exact case-insensitive match
def findMemberByName(name):
    allMembers = getChainAllMemberInfo()
    match = [member for member in allMembers if member[0].lower() == name.lower()]
    return match

# get account UID from /me endpoint
def getMe():
    response = requests.get(
        f"{SIMPLY_PLURAL_BASE_URL}/me",
        headers=headers,
        data=payload,
        timeout=10,
    )
    data = response.json()
    UID = data["id"]
    return UID


def getAllMemberInfo(UID):
    memberListConc = []
    response = requests.get(
        f"{SIMPLY_PLURAL_BASE_URL}/members/{UID}",
        headers=headers,
        data=payload,
        timeout=10,
    )
    system = response.json()
    for member in system:
        content = member["content"]
        # check if the contents of pronouns after stripping whitespace is not empty
        # do this to filter out test or uncomplete members
        if content["pronouns"].strip():
            memberListConc.append(
                (
                    content["name"],
                    content["avatarUrl"],
                    content["pronouns"],
                    content["desc"],
                )
            )
    return memberListConc


def getChainAllMemberInfo():
    UID = getMe()
    AllMemberInfo = getAllMemberInfo(UID)
    return AllMemberInfo


# here and below would be in other files
# replace with your own path, start at the root of the project
token = getToken("token.json")

# set up for making requests
payload = {}
headers = {"Authorization": token["SimplyPluralAPIKey"]}

all = getChainCustomFronterInfo()
print(all)