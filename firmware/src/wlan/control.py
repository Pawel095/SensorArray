import network
from config import CONFIG

ap = network.WLAN(network.AP_IF)
cl = network.WLAN(network.STA_IF)


def startAP(ssid, password, security=network.AUTH_WPA2_PSK):
    ap.active(True)
    ap.config(essid=ssid, password=password, authmode=security)
    print(ap.ifconfig())


def stopAP():
    ap.active(False)


def connectCL():
    cl.active(True)

    ssid = CONFIG.get("ssid")
    passw = CONFIG.get("pass")

    if ssid == "" or passw == "":
        return False

    cl.connect(ssid, passw)


def statusCL():
    return cl.status()


def get_ipCL():
    return cl.ifconfig()[0]


def disconnectCL():
    cl.disconnect()


def disableCL():
    cl.active(False)
