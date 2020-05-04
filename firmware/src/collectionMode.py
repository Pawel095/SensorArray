from wlan.control import stopAP, connectCL, cl as client
from machine import Pin, PWM
from config import CONFIG
from dht11.measure import Measure
from server import Server, Response, View
import uasyncio as asyncio

app = Server()
loop = asyncio.get_event_loop()


class CollectionMode:
    def __init__(self):
        self.green = Pin(2, Pin.OUT)
        self.red = Pin(0, Pin.OUT)
        task = ping_led_until_true(self.green, client.isconnected, 10)
        loop.create_task(task)
        app.register_func(index, "/", ["GET"])
        app.register_func(jquery, "/jquery.js", ["GET"])
        app.register_func(mainJs, "/main.js", ["GET"])
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


async def send_data_to_server():
    await asyncio.sleep(10)


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
