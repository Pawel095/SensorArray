from rest_framework.test import APITestCase

from api.utils.timestampDefaultValues import generate_timestamps

from datetime import datetime
import time
import pytz

# Create your tests here.


class GenerateTimestampTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        class Request:
            def __init__(self):
                self.method = "GET"
                self.GET = {}

        cls.request = Request()

        return super().setUpTestData()

    def test_sanity(self):
        assert 1 == 1

    def test_both_timestamps_correct(self):
        rq = self.request
        rq.GET = {"start": time.time() - 3600, "end": time.time() - 600}

        st = self.request.GET["start"]
        et = self.request.GET["end"]

        # both timestamps specified
        startDT, endDT = generate_timestamps(rq)
        assert startDT == datetime.fromtimestamp(st, tz=pytz.utc)
        assert endDT == datetime.fromtimestamp(et, tz=pytz.utc)

    def test_only_start_timestamp_specified(self):
        rq = self.request

        rq.GET = {"start": time.time() - 3600}

        st = self.request.GET["start"]
        et = self.request.GET["start"] + 3600

        startDT, endDT = generate_timestamps(rq)
        assert startDT == datetime.fromtimestamp(st, tz=pytz.utc)
        assert endDT == datetime.fromtimestamp(et, tz=pytz.utc)

    def test_only_end_timestamp_specified(self):
        rq = self.request

        rq.GET = {"end": time.time()}

        st = self.request.GET["end"] - 3600
        et = self.request.GET["end"]

        startDT, endDT = generate_timestamps(rq)
        assert startDT == datetime.fromtimestamp(st, tz=pytz.utc)
        assert endDT == datetime.fromtimestamp(et, tz=pytz.utc)

    def test_no_timestamps_specified(self):
        rq = self.request

        rq.GET = {}

        startDT, endDT = generate_timestamps(rq)
        assert startDT.timestamp() + 3600 == endDT.timestamp()
