import tinyweb
from wlan.control import startAP, disableCL
import util
from config import CONFIG, save_config
import uasyncio as asyncio

app = tinyweb.webserver()
loop = asyncio.get_event_loop()


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
        print("setup mode enabled")
        # TODO: run server here
        print("server stopped")


@app.route("/")
async def staticFiles(req, resp):
    await resp.send_file("/setupStaticFiles/index.html")


@app.route("/kill")
async def stop(req, resp):
    await resp.start_html()
    await resp.send("<html><body>Server stopped</body></html>\n")
