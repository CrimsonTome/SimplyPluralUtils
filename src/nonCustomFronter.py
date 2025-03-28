# returns a list of fronter IDs from the fronters list
from src.common import getAllFronterID
from src.sessionSetup import SIMPLY_PLURAL_BASE_URL, headers, payload


import requests

from src.user import getMe


def craftFronterIDList(fronters):
    fronter_id_list = [
        item["content"]["member"]
        for item in fronters
        if not item["content"].get("custom", False)
    ]
    return fronter_id_list


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


def getChainNonCustomFronterInfo():
    fronterIDs = getAllFronterID()
    fronterIDList = craftFronterIDList(fronterIDs)
    UID = getMe()
    fronterList = getNonCustomFronters(fronterIDList, UID)
    return fronterList