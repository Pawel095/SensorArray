from machine import Pin
import dht
import time


class Measure:
    def __init__(self, lock, led=None):
        self.MEASUREMENT_DELAY = 5
        self.lock = lock
        self.led = led

        self.d = dht.DHT11(Pin(15, Pin.IN, Pin.PULL_UP))
        self.lastTime = time.time() - self.MEASUREMENT_DELAY
        self.lastResult = {}

    async def __call__(self):
        await self.lock.acquire()
        if self.lastTime + self.MEASUREMENT_DELAY < time.time():
            if self.led is not None:
                self.led.on()

            try:
                self.d.measure()
                self.lastResult = {
                    "temperature": self.d.temperature(),
                    "humidity": self.d.humidity(),
                }
                self.lastTime = time.time()

            except OSError as e:
                print("error reading sensor")
                self.lastResult = {"error": e}

            if self.led is not None:
                self.led.off()

        self.lock.release()
        return self.lastResult
