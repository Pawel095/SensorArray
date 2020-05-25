from rest_framework.test import APITestCase

from api.models import RegisteredSensors, LoggedData
import random

from sensorApi.settings import IDENTIFICATION_STRING

# Create your tests here.


def add_sensors(cls):
    s1 = {
        "name": "tm1xpgiizrinoxo6w2zd",
        "display_name": "Sensor 1",
        "description": "Data collected 2020-05-07 to 2020-05-08",
    }
    s2 = {
        "name": "7jisve665ybr8jbplhqz",
        "display_name": "Sensor2",
        "description": "Collection from 2020-05-11 to 2020-05-12",
    }
    cls.s1 = RegisteredSensors(**s1)
    cls.s1.save()
    cls.s2 = RegisteredSensors(**s2)
    cls.s2.save()


def add_sensor_data(cls):
    s1data = [
        LoggedData(
            temperature=random.randint(0, 60),
            humidity=random.randint(0, 100),
            sensor=cls.s1,
        )
        for i in range(200)
    ]
    s2data = [
        LoggedData(
            temperature=random.randint(0, 60),
            humidity=random.randint(0, 100),
            sensor=cls.s2,
        )
        for i in range(200)
    ]
    [s.save() for s in s1data]
    [s.save() for s in s2data]


class SanityTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        add_sensors(cls)
        add_sensor_data(cls)
        return super().setUpTestData()

    def test_sanity(self):
        sensor = RegisteredSensors.objects.get(pk=self.s1.pk)
        assert sensor == self.s1


class IdentifySelfTests(APITestCase):
    def test_identify_self(self):
        result = self.client.get("/api/identify/")
        assert result.status_code == 200
        assert result.data == IDENTIFICATION_STRING


class RegisterSensorTests(APITestCase):
    def test_register_new_sensor_valid_data(self):
        raise NotImplementedError

    def test_register_new_sensor_invalid_data(self):
        raise NotImplementedError


class DataPerSensorTests(APITestCase):
    def test_post_not_registered_sensor(self):
        raise NotImplementedError

    def test_post_registered_sensor_bad_data(self):
        raise NotImplementedError

    def test_post_registered_sensor_correct_data(self):
        raise NotImplementedError

    def test_get_data_for_existing_sensor(self):
        raise NotImplementedError

    def test_data_for_not_existing_sensor(self):
        raise NotImplementedError


class AllDataTests(APITestCase):
    def test_get_all_logged_data(self):
        raise NotImplementedError


class SensorsListTests(APITestCase):
    def test_(self):
        raise NotImplementedError
    