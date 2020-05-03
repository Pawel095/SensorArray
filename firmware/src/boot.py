import gc
import os

gc.enable()
# create status file if not existing
if "state" not in os.listdir():
    print("creating new state file")
    data = """{"state":"setup","ssid":"","pass":"","id":""}"""
    f = open("state", "w")
    f.write(data)
    f.close()
print("\n")
