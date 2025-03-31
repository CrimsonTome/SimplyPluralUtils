from src.common import getAllFronters
from src.sessionSetup import SIMPLY_PLURAL_BASE_URL, headers, payload
from src.user import getMe

import requests


def craftFronterIDList(fronters):
    """
    Extract the non custom fronter IDs from information on them.

    Paramaters:
        fronters(list): A list of dictionaries containing fronter information.

    Returns:
        fronterID(list): A list of member IDs for non custom fronters.
    """
    fronterIDList = [
        item["content"]["member"]
        for item in fronters
        if not item["content"].get("custom", False)
    ]
    return fronterIDList


def getNonCustomFronters(fronterList, UID):
    """
    Gets specific information about non fronters 
    and returns the joined list.

    Parameters:
        fronterList (list): List of non custom fronter IDs.
        UID (str): The unique identifier of the authenticated user.

    Returns:
        fronterListConc (list): A list of information on non custom fronters.
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


def getChainNonCustomFronterInfo():
    """
    Chain multiple function calls to fetch custom fronter details.    
    """
    fronterIDs = getAllFronters()
    fronterIDList = craftFronterIDList(fronterIDs)
    UID = getMe()
    fronterList = getNonCustomFronters(fronterIDList, UID)
    return fronterList
