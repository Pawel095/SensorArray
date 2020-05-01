import ujson as json

with open("state") as f:
    CONFIG = json.loads(f.read())
    f.close()
    print("config loaded: {}".format(CONFIG))


def save_config():
    with open("state", "w") as f:
        print("writing {}\n".format(json.dumps(CONFIG)))
        f.write(json.dumps(CONFIG))
        f.close()
