from setupMode import SetupMode
from config import CONFIG
from wlan.control import connectCL


if CONFIG["state"] == "setup":
    SetupMode()()
