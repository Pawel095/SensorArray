import network
from config import CONFIG


def startAP(ssid, password, security=network.AUTH_WPA2_PSK):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password, authmode=security)
    ap.active(True)
    print(ap.ifconfig())


def stopAP():
    ap = network.WLAN(network.AP_IF)
    ap.active(False)


def connectCL():
    cl = network.WLAN(network.STA_IF)
    cl.active(True)

    ssid = CONFIG.get("ssid")
    passw = CONFIG.get("pass")

    if ssid == "" or passw == "":
        raise ConnectionError("ssid or password not available")

    cl.connect(ssid, passw)


def disconnectCL():
    cl = network.WLAN(network.STA_IF)
    cl.disconnect()


def disableCL():
    cl = network.WLAN(network.STA_IF)
    cl.active(False)
