from wlan.control import stopAP, connectCL
from config import CONFIG
from server import Server, Response, View
import uasyncio as asyncio

app = Server()


class CollectionMode:
    def __init__(self):
        stopAP()
        connectCL()
        print("INIT")

    def __call__(self):
        print("Collection mode started")
        app.run()
        print("server stopped")

async def send_data_to_server():
    
    await asyncio.sleep(10)

def index(req):
    return Response(status=200, body=open("setupModeStatic/index.html"))


def mainJs(req):
    headers = {"Content-Type": "application/javascript"}
    return Response(status=200, body=open("setupModeStatic/main.js"), headers=headers)


def jquery(req):
    headers = {
        "Content-Type": "application/javascript",
        "Cache-Control": "max-age=2592000, public",
    }
    return Response(status=200, body=open("jquery/jquery.js"), headers=headers)
