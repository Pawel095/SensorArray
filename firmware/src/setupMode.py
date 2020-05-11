from wlan.control import startAP, disableCL, get_ipCL
import util
from config import CONFIG, save_config
from server import Server, Response, View
from wlan.control import statusCL, connectCL
import ujson as json
import uasyncio as asyncio
from uasyncio.lock import Lock
import urequests as requests
from machine import Pin, reset

server_lock = Lock()
app = Server(server_lock)

green = Pin(2, Pin.OUT)
red = Pin(0, Pin.OUT)


class SetupMode:
    def __init__(self):
        print("INIT")
        if CONFIG.get("id") == "":
            CONFIG["id"] = util.generate_random_name()
            save_config()

        ssid = "Sensor {}".format(CONFIG["id"])
        password = "SensorGrid"

        disableCL()
        startAP(ssid, password)
        red.on()

        app.register_func(index, "/", ["GET"])
        app.register_func(jquery, "/jquery.js", ["GET"])
        app.register_func(mainJs, "/main.js", ["GET"])
        app.register_func(check_server_and_register, "/api/register", ["POST"])
        app.register_view(connectionApi(), "/api/connect")

    def __call__(self):
        print("setup mode enabled")
        app.run()
        print("server stopped")


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


def check_server_and_register(req):
    try:
        data = json.loads(req.body)
    except ValueError:
        return Response(status=400)

    if "ip" in data:
        try:
            resp = requests.get("http://{}/api/identify/".format(data["ip"]))
        except OSError as e:
            return Response(body=str(e), status=404)

    if resp.status_code == 200:
        if resp.text == '"DataCollectorV1"':
            try:
                resp = requests.post(
                    "http://{}/api/register/".format(data["ip"]),
                    json={
                        "name": CONFIG["id"],
                        "display_name": data.get("display_name", CONFIG["id"]),
                        "description": data.get("description"),
                    },
                )
                print(resp.text)
            except OSError as e:
                return Response(body=str(e), status=400)
            else:
                if resp.status_code == 201:
                    CONFIG["server"] = data["ip"]
                    CONFIG["state"] = "collector"
                    save_config()
                    asyncio.get_event_loop().create_task(scheduleReset(3))
                    return Response(status=200, body=str(get_ipCL()))
                else:
                    return Response(body=str(resp.text), status=400)
    return Response(status=400)


async def scheduleReset(delay):
    await asyncio.sleep(delay)
    reset()


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
    return Response(
        status=200, body=open("jquery/jquery-3.5.1.min.js"), headers=headers
    )
