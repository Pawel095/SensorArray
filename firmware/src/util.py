import os

chars = list("qwertyuiopasdfghjklzxcvbnm1234567890")


def generate_random_name(length=20):
    ret = []
    for i in range(length):
        number = int.from_bytes(os.urandom(1), "little")
        ret.append(chars[number % 36])
    return "".join(ret)
