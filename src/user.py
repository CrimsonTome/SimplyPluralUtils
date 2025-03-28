from src.sessionSetup import SIMPLY_PLURAL_BASE_URL, headers, payload


import requests


def getUID(fronters):
    """
    Get the unique identifier for an authenticated user.

    Parameters:
        fronters(list): A list of the current fronters with all their attributes.

    Returns:
        UID(str): the unique identifier, also known as the system ID

    Notes: 
        It is not recommended to use this method,
        if there are no fronters it will fail. Prefer getMe instead
    """
    UID = fronters[0]["content"]["uid"]
    return UID


def getMe():
    """Get the unique identifier for an authenticated user."""
    response = requests.get(
        f"{SIMPLY_PLURAL_BASE_URL}/me",
        headers=headers,
        data=payload,
        timeout=10,
    )
    data = response.json()
    UID = data["id"]
    return UID
