import gc
import uasyncio as asyncio

METHODS = ["GET", "POST", "PUT", "DELETE"]


class Request:
    def __init__(self, request_string: str):
        lines = request_string.split("\r\n")
        t = lines[0].split(" ")
        try:
            self.method = t[0]
            self.url = t[1]
            self.protocol = t[2]
        except IndexError:
            print("request empty")

        self.headers = []
        for line in lines[1:]:
            if line == "":
                break
            t = line.split(":")
            self.headers.append({t[0]: t[1]})

        # parse params in url
        t = self.url.split("?")
        try:
            self.route = t[0]
            params = t[1]

            self.params = []
            param_lines = params.split("&")
            for p in param_lines:
                k, v = p.split("=")
                self.params.append({k: v})

        except ValueError:
            # no params in request, url includes ?
            self.route = self.url[:-1]
            self.params = []

        except IndexError:
            # no params in request
            self.route = self.url
            self.params = []

        self.body = ""
        flag = False
        for line in lines:
            if line == "":
                flag = True

            if flag:
                self.body += str(line)

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
        self.body = str(kwargs.get("body", ""))

    def to_bytes(self):
        yield "{} {} {}\n".format(self.protocol, self.status, self.reason).encode()
        for k, v in self.headers.items():
            yield "{}:{}\n".format(k, v).encode()

        yield "\n".encode()

        if isinstance(self.body, str):
            yield (str(self.body)).encode()
        else:
            buf = bytearray(1024)
            while True:
                gc.collect()
                size = self.body.readinto(buf)
                if size == 0:
                    break
                yield bytes(buf[:size])


class Server:
    def __init__(self):
        self.routes = []

    async def handler(self, reader, writer):
        request_bytes = await reader.read(-1)
        req = Request(request_bytes.decode())
        addr = reader.get_extra_info("peername")
        print("{}: '{}' from {}".format(req.method, req.route, addr[0]))
        resp = Response(status=404)

        for r in self.routes:
            if r["route"] == req.route:
                view = r.get("view")
                func = r.get("func")

                if view is not None:
                    resp = view.runMethod(req)
                    print("View: {}".format(r["view"]))

                elif func is not None:
                    if req.method in r["methods"]:
                        print("Func {}".format(r["func"]))
                        resp = func(req)
                    else:
                        resp = Response(status=405)

        for b in resp.to_bytes():
            await writer.awrite(b)
        await writer.aclose()
        await reader.aclose()

    def register_view(self, view, route):
        """set function for foute
        """
        print("registering {}".format({"view": str(view), "route": route}))
        self.routes.append({"view": view, "route": route})

    def register_func(self, func, route, methods):
        print(
            "registering {}".format(
                {"func": str(func), "route": route, "methods": methods}
            )
        )
        self.routes.append({"func": func, "route": route, "methods": methods})

    def run(self):
        task = asyncio.start_server(self.handler, "0.0.0.0", 80, backlog=2)
        loop = asyncio.get_event_loop()
        loop.create_task(task)
        loop.run_forever()


class View:
    description = "default view"

    def runMethod(self, request: Request):
        method = request.method
        if method == "HEAD":
            return Response(status=200)

        if method not in METHODS:
            return Response(status=501)

        if method == "GET":
            return self.get(request)

        if method == "POST":
            return self.post(request)

        if method == "PUT":
            return self.put(request)

        if method == "DELETE":
            return self.delete(request)

    def get(self, request):
        return Response(status=405)

    def post(self, request):
        return Response(status=405)

    def put(self, request):
        return Response(status=405)

    def delete(self, request):
        return Response(status=405)

    def __str__(self):
        return self.description
