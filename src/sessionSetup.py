import json
from pathlib import Path


def getToken(userPath):
    """
    Get the Simply Plural API key from the file specified by the user.

    Paraters:
        userPath(str): The path to the token file, starting at the repo root.

    Returns:
        token(dict): The token loaded as JSON from the file.

    Notes:
        The token JSON should be in the format specified in token.example.json
    """
    tokenPath = Path(userPath)
    with tokenPath.open(encoding="utf-8") as tokenFile:
        token = json.load(tokenFile)
        return token


SIMPLY_PLURAL_BASE_URL = "https://api.apparyllis.com/v1"

# these should be moved into the client's code probably
token = getToken("token.json")

payload = {}
headers = {"Authorization": token["SimplyPluralAPIKey"]}
