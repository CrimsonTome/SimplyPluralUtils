from common import getAllFronters
from sessionSetup import SIMPLY_PLURAL_BASE_URL, headers, payload
from user import getMe

import requests


# Note: Some things here are broken and need to be investigated


def craftCustomFronterIDList(fronters):
    """
    Extract the custom fronter IDs from information on them.

    Paramaters:
        fronters(list): A list of dictionaries containing fronter information.

    Returns:
        customFronterIDList(list): A list of member IDs for custom fronters.
    """
    customFronterIDList = [
        item["content"]["member"]
        for item in fronters
        if item["content"].get("custom", False)
    ]
    return customFronterIDList


def getCustomFronters(customFronterList, UID):
    """
    Gets specific information about custom fronters
    and returns the joined list.

    Parameters:
        customFronterList (list): List of custom fronter IDs.
        UID (str): The unique identifier of the authenticated user.

    Returns:
        customFronterListConc (list): A list of information on custom fronters.
    """
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


def getChainCustomFronterInfo():
    """
    Chain multiple function calls to fetch custom fronter details.
    """
    customFronterIDs = getAllFronters()
    customFronterIDList = craftCustomFronterIDList(customFronterIDs)
    UID = getMe()
    customFronterList = getCustomFronters(customFronterIDList, UID)
    return customFronterList
