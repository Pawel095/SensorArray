import ujson as json
# from setupMode import SetupMode
from config import CONFIG
import server
from wlan.control import connectCL


if CONFIG['state'] == "setup":
    # SetupMode()()
    connectCL()
    server.run()
