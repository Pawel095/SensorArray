from setupMode import SetupMode
from config import CONFIG


if CONFIG["state"] == "setup":
    SetupMode()()

elif CONFIG["state"] == "collector":
    pass
    # send data to backend
