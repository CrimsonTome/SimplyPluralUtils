from src.sessionSetup import SIMPLY_PLURAL_BASE_URL, headers, payload


import requests


# returns the stripped system ID using the first fronter
# you can also use the /me endpoint to get the system ID with some more filtering
# this will fail if there are no fronters, prefer the newer getMe instead!
def getUID(fronters):
    return fronters[0]["content"]["uid"]


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
