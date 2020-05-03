from wlan.control import startAP, disableCL
import util
from config import CONFIG, save_config
import uasyncio as asyncio
from server import Server, Response

app = Server()


class SetupMode:
    def __init__(self):
        print("INIT")

    def __call__(self):
        if CONFIG.get("id") == "":
            CONFIG["id"] = util.generate_random_name()
            save_config()

        ssid = "Sensor {}".format(CONFIG["id"])
        password = "SensorGrid"

        disableCL()
        startAP(ssid, password)
        app.register_func(index, "/", ["GET"])
        app.register_func(jquery, "/jquery.js", ["GET"])
        app.register_func(mainJs, "/main.js", ["GET"])
        print("setup mode enabled")
        app.run()
        print("server stopped")


def index(req):
    return Response(status=200, body=open("setupModeStatic/index.html"))

def mainJs(req):
    return Response(status=200, body=open("setupModeStatic/main.js"))

def jquery(req):
    return Response(status=200, body=open("jquery/jquery.js"))

