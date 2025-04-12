import time
import websocket
import json
import threading

from sessionSetup import getToken


def onMessage(ws, message):
    print("Received:", message)
    if "results" in message:
        data = json.loads(message)
        # Get ID of the member in question
        id = data["results"][0]["id"]
        print(id)


def onError(ws, error):
    print("Error:", error)


def onClose(ws, close_status_code, close_msg):
    print("Closed:", close_status_code, close_msg)


def onOpen(ws):
    # Authenticate
    token = getToken("token.json")
    authPayload = json.dumps(
        {"op": "authenticate", "token": token["SimplyPluralAPIKey"]}
    )
    print("Sending authentication data")
    ws.send(authPayload)

    # Keep connection alive
    def keepAlive():
        while True:
            print("Sending keep alive ping")
            ws.send("ping")
            time.sleep(10)

    threading.Thread(target=keepAlive).start()


def main():
    # Connect to the WebSocket
    ws_url = "wss://api.apparyllis.com/v1/socket"
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        ws_url, on_message=onMessage, on_error=onError, on_close=onClose
    )
    ws.on_open = onOpen
    ws.run_forever()


if __name__ == "__main__":
    main()
