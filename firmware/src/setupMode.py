from wlan.control import startAP, disableCL
import util
from config import CONFIG, save_config
from server import Server, Response, View
from wlan.control import statusCL, disableCL, connectCL
import uasyncio as asyncio
import ujson as json

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
        app.register_view(connectionApi(), "/api/connect")
        app.register_func(look_for_backend, "/api/search", ["POST"])
        print("setup mode enabled")
        app.run()
        print("server stopped")


def look_for_backend(request):
    return Response(status=200)


class connectionApi(View):
    def get(self, request):
        status = statusCL()
        return Response(body=str(status), status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
        except ValueError:
            return Response(status=400)

        if "ssid" in data and "pass" in data:
            CONFIG["ssid"] = data["ssid"]
            CONFIG["pass"] = data["pass"]
            save_config()

        connectCL()
        return Response(status=200)

    def delete(self, request):
        disableCL()
        return Response(status=200)


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
