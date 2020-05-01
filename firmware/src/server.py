import uasyncio as asyncio


def run():
    task = asyncio.start_server(handler, "0.0.0.0", 80, backlog=2)
    loop = asyncio.get_event_loop()
    loop.create_task(task)
    loop.run_forever()


class Request:
    def __init__(self, request_string: str):
        lines = request_string.split("\r\n")
        t = lines[0].split(" ")
        self.method = t[0]
        self.url = t[1]
        self.protocol = t[2]
        self.headers = []
        for l in lines[1:]:
            if l == "":
                break
            t = l.split(":")
            self.headers.append({t[0]: t[1]})

    def __str__(self):
        ret = "method:{}\r\nURL:{}\r\n".format(self.method, self.url)
        for h in self.headers:
            ret += "{}\r\n".format(h)
        return ret


class Response:
    def __init__(self, **kwargs):
        self.protocol = "HTTP/1.1"
        self.status = kwargs.get("status", 500)
        self.reason = kwargs.get("reason", "")
        self.headers = kwargs.get("headers", {})
        self.body = kwargs.get("body", "")

    def to_bytes(self):
        ret = "{} {} {}\n".format(self.protocol, self.status, self.reason)
        for k, v in self.headers.items():
            ret += "{}:{}\n".format(k, v)
        ret += "\n"+str(self.body)
        return ret.encode()


async def handler(reader, writer):
    request_bytes = await reader.read(-1)
    req = Request(request_bytes.decode())
    addr = reader.get_extra_info("peername")
    print("{}: '{}' from {}".format(req.method, req.url, addr[0]))

    # find View, execute and return response

    resp = Response(status=720, reason="Unpossible", body="test1")
    await writer.awrite(resp.to_bytes())
    await writer.aclose()
    await reader.aclose()
    return


class View:
    def get(self, request):
        return Response(status=405)

    def post(self, request):
        return Response(status=405)

    def gut(self, request):
        return Response(status=405)

    def delete(self, request):
        return Response(status=405)
