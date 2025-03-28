# return the token from the user's token file
import json
from pathlib import Path


def getToken(userPath):
    tokenPath = Path(userPath)
    with tokenPath.open(encoding="utf-8") as tokenFile:
        token = json.load(tokenFile)
        return token


SIMPLY_PLURAL_BASE_URL = "https://api.apparyllis.com/v1"

# these should be moved into the client's code probably
token = getToken("token.json")

payload = {}
headers = {"Authorization": token["SimplyPluralAPIKey"]}