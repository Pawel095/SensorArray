from setupMode import SetupMode
from config import CONFIG


if CONFIG["state"] == "setup":
    SetupMode()()
