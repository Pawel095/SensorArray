import ujson as json
from setupMode import SetupMode
from config import CONFIG
import server


if CONFIG['state']=="setup":
    # SetupMode()()
    server.run()

