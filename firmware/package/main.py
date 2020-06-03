from setupMode import SetupMode
from collectionMode import CollectionMode
from config import CONFIG


if CONFIG["state"] == "setup":
    SetupMode()()

elif CONFIG["state"] == "collector":
    CollectionMode()()
