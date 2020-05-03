import network
from config import CONFIG

ap = network.WLAN(network.AP_IF)
cl = network.WLAN(network.STA_IF)


def startAP(ssid, password, security=network.AUTH_WPA2_PSK):
    ap.config(essid=ssid, password=password, authmode=security)
    ap.active(True)
    print(ap.ifconfig())


def stopAP():
    ap.active(False)


def connectCL():
    cl.active(True)

    ssid = CONFIG.get("ssid")
    passw = CONFIG.get("pass")

    if ssid == "" or passw == "":
        raise ConnectionError("ssid or password not available")

    cl.connect(ssid, passw)


def statusCL():
    return cl.status()


def disconnectCL():
    cl.disconnect()


def disableCL():
    cl.active(False)
