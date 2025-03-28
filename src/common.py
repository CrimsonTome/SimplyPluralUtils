from src.sessionSetup import SIMPLY_PLURAL_BASE_URL, headers, payload
from src.user import getMe

import requests


# returns a list of all fronter info from the /fronters endpoint
# https://docs.apparyllis.com/docs/api/get-current-fronters-self
def getAllFronters():
    response = requests.get(
        f"{SIMPLY_PLURAL_BASE_URL}/fronters", headers=headers, data=payload, timeout=10
    )
    fronters = response.json()
    return fronters


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


def getChainAllMemberInfo():
    UID = getMe()
    AllMemberInfo = getAllMemberInfo(UID)
    return AllMemberInfo


# returns a list containing fronter information for those that match the query
# looks for an exact case-insensitive match
def findMemberByName(name):
    allMembers = getChainAllMemberInfo()
    match = [member for member in allMembers if member[0].lower() == name.lower()]
    return match


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
