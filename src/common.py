from sessionSetup import SIMPLY_PLURAL_BASE_URL, headers, payload
from user import getMe

import requests


def getAllFronters():
    """
    Get a list of all fronter information
    and returns the response as a list of JSON.
    """
    response = requests.get(
        f"{SIMPLY_PLURAL_BASE_URL}/fronters", headers=headers, data=payload, timeout=10
    )
    fronters = response.json()
    return fronters


def getAllFronterInfo(fronterList, customFronterList, UID):
    """
    Gets specific information about regular and custom fronters
    and returns the joined list.

    Parameters:
        fronterList (list): List of regular fronter IDs.
        customFronterList (list): List of custom fronter IDs.
        UID (str): The unique identifier of the authenticated user.

    Returns:
        fronterListConc (list): A list of information on all fronters.
    """
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
    """
    Retrieve information for all members in a system.

    Returns:
        AllMemberInfo (list): A list of all member information
        retrieved by getAllMemberInfo.
    """
    UID = getMe()
    AllMemberInfo = getAllMemberInfo(UID)
    return AllMemberInfo


def findMemberByName(name):
    """
    Search for members by name with an exact case-insensitive match

    Parameters:
        name (str): The name to search for.

    Returns:
        match (list): A list of members matching the provided name
    """
    allMembers = getChainAllMemberInfo()
    match = [member for member in allMembers if member[0].lower() == name.lower()]
    if match:
        return match[0]
    else:
        return ""


def getAllMemberInfo(UID):
    """
    Get information for all members in the system.

    Parameters:
        UID (str): The unique identifier of the authenticated user.

    Returns:
        AllMemberInfo (list): A list of all member information.
    """
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
        if "pronouns" in content:
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


def getFriendFronters(FUID):
    """
    Get current fronters of a friend

    Parameters:
        FUID (str): The unique identifier of the friend.

    Returns:
        friendFronters (str): A list (handled as a string) of the current fronters
        of the friend
    """
    response = requests.get(
        f"{SIMPLY_PLURAL_BASE_URL}/friend/{FUID}/getFrontValue",
        headers=headers,
        data=payload,
        timeout=10,
    )
    content = response.json()
    friendFronters = content["frontString"]
    return friendFronters
