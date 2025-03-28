# returns a list of custom fronter IDs from the fronters list
from src.common import getAllFronters
from src.sessionSetup import SIMPLY_PLURAL_BASE_URL, headers, payload
from src.user import getMe

import requests


def craftCustomFronterIDList(fronters):
    custom_fronter_id_list = [
        item["content"]["member"]
        for item in fronters
        if item["content"].get("custom", False)
    ]
    return custom_fronter_id_list


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


# TODO: this is currently broken. need to fix later
def getChainCustomFronterInfo():
    customFronterIDs = getAllFronters()
    customFronterIDList = craftCustomFronterIDList(customFronterIDs)
    UID = getMe()
    customFronterList = getCustomFronters(customFronterIDList, UID)
    return customFronterList
