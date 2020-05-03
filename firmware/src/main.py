import ujson as json
# from setupMode import SetupMode
from config import CONFIG
from server import Server, View, Response
from wlan.control import connectCL


class TestView(View):
    description = "simple test view"

    def get(self, request):
        f = open("index.html")
        headers = {"Content-Type": "text/html",
                   "Cache-Control": "max-age=2592000, public"}
        return Response(status=200, body=f, headers=headers)


if CONFIG["state"] == "setup":
    connectCL()
    app = Server()
    app.register_view(TestView(), "/")
    app.run()
