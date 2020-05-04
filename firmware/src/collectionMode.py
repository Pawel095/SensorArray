from wlan.control import stopAP, connectCL, cl as client
from machine import Pin, PWM
from config import CONFIG
from dht11.measure import Measure
from server import Server, Response
import ujson as json
import gc
import uasyncio as asyncio
import urequests as requests
from uasyncio.lock import Lock

green = Pin(2, Pin.OUT)
red = Pin(0, Pin.OUT)

server_lock = Lock()

app = Server(server_lock)
loop = asyncio.get_event_loop()

reading_lock = Lock()
temp_reader = Measure(reading_lock, led=red)


class CollectionMode:
    def __init__(self):
        task = ping_led_until_true(green, client.isconnected, 10)
        loop.create_task(task)
        task = send_data_to_server()
        loop.create_task(task)

        app.register_func(index, "/", ["GET"])
        app.register_func(jquery, "/jquery.js", ["GET"])
        app.register_func(mainJs, "/main.js", ["GET"])
        app.register_afunc(single_reading, "/api/getReading", ["GET"])

        stopAP()
        connectCL()
        print("INIT")

    def __call__(self):
        print("Collection mode started")
        app.run()
        print("server stopped")


async def ping_led_until_true(led: Pin, condition, freq, delay=1000):
    pwm = PWM(led)
    pwm.freq(freq)
    pwm.duty(511)

    await asyncio.sleep_ms(delay)
    while not condition:
        await asyncio.sleep_ms(delay)

    pwm.deinit()
    return


async def single_reading(req):
    data = await temp_reader()
    return Response(body=json.dumps(data), status=200)


async def send_data_to_server():
    while True:
        await server_lock.acquire()
        url = "http://{}/api/log_data/{}/".format(CONFIG["server"], CONFIG["id"])
        gc.collect()
        body = json.dumps(await temp_reader())
        print("{} :: {}".format(url, body))
        try:
            resp = requests.post(
                url, data=body, headers={"Content-Type": "application/json"}
            )
        except OSError as e:
            print("error sending data {}".format(e))
        else:
            try:
                print(resp.text)
            except MemoryError:
                print("response too big")
        gc.collect()
        server_lock.release()
        await asyncio.sleep(15)


def index(req):
    return Response(status=200, body=open("collectionStaticFiles/index.html"))


def mainJs(req):
    headers = {"Content-Type": "application/javascript"}
    return Response(
        status=200, body=open("collectionStaticFiles/main.js"), headers=headers
    )


def jquery(req):
    headers = {
        "Content-Type": "application/javascript",
        "Cache-Control": "max-age=2592000, public",
    }
    return Response(status=200, body=open("jquery/jquery.js"), headers=headers)
