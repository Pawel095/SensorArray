import tinyweb
from wlan.control import startAP, disableCL
import util
from config import CONFIG, save_config
import uasyncio as asyncio
from uasyncio.event import Event
import ujson as json

app = tinyweb.webserver(host="0.0.0.0", port=80)
loop = asyncio.get_event_loop()
stop_event = Event()


async def start_webserver():
    await app.start()


async def wait_for_event(e):
    await e.wait()
    e.clear()


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
        asyncio.run(start_webserver())
        loop.run_until_complete(wait_for_event(stop_event))
        print("server stopped")


@app.route("/")
async def staticIndex(req, resp):
    await resp.send_file("/setupStaticFiles/index.html")


@app.route("/main.js")
async def staticMainJs(req, resp):
    await resp.send_file("/setupStaticFiles/main.js")


@app.route("/jquery.js")
async def staticjJquery(req, resp):
    await resp.send_file("/jquery.js")


@app.route("/api/connect", methods=["POST"])
async def try_to_connect(req, resp):
    await resp.send("asd")


@app.route("/t", save_headers=["Content-Length", "Content-Type"], methods=["POST"])
async def test(req, resp):
    print("/t")
    print(dir(req.reader))
    data = await req.read_parse_form_data()
    print(data)
    await resp.send(json.dumps(data))


@app.route("/kill")
async def stop(req, resp):
    await resp.start_html()
    await resp.send("<html><body>Server stopped</body></html>\n")
    stop_event.set()
