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
        dataCount = LoggedData.objects.count()
        assert sensor == self.s1
        assert dataCount == 400


class IdentifySelfTests(APITestCase):
    def test_identify_self(self):
        result = self.client.get("/api/identify/")
        assert result.status_code == 200
        assert result.data == IDENTIFICATION_STRING


class RegisterSensorTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        add_sensors(cls)
        return super().setUpTestData()

    def test_register_new_sensor_valid_data(self):
        data = {"name": "ajusghdaklsgjd", "display_name": "test1"}
        sensors_before = RegisteredSensors.objects.count()
        result = self.client.post("/api/register/", data=data)
        sensors_after = RegisteredSensors.objects.count()

        assert result.status_code == 201
        assert sensors_before + 1 == sensors_after

    def test_register_new_sensor_invalid_data(self):
        data = {"display_name": "test1"}
        sensors_before = RegisteredSensors.objects.count()
        result = self.client.post("/api/register/", data=data)
        sensors_after = RegisteredSensors.objects.count()

        assert result.status_code == 400
        assert sensors_before == sensors_after

    def test_register_sensor_name_already_taken(self):
        data = {"name": self.s1.name, "display_name": "test1"}
        sensors_before = RegisteredSensors.objects.count()
        result = self.client.post("/api/register/", data=data)
        sensors_after = RegisteredSensors.objects.count()

        assert result.status_code == 400
        assert sensors_before == sensors_after


class DataPerSensorTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        add_sensors(cls)
        add_sensor_data(cls)
        return super().setUpTestData()

    def test_post_not_registered_sensor(self):
        data = {
            "temperature": 20,
            "humidity": 46,
        }
        data_before = LoggedData.objects.count()
        result = self.client.post(
            "/api/log_data/ThisSensorNameIsNotInTheDatabase/", data
        )
        data_after = LoggedData.objects.count()

        assert data_after == data_before
        assert result.status_code == 401

    def test_post_registered_sensor_bad_data(self):
        data = {
            "temasdaperature": 20,
            "humidiasdadaty": 46,
        }
        data_before = LoggedData.objects.count()
        result = self.client.post(f"/api/log_data/{self.s1.name}/", data)
        data_after = LoggedData.objects.count()

        assert data_after == data_before
        assert result.status_code == 400

    def test_post_registered_sensor_correct_data(self):
        data = {
            "temperature": 20,
            "humidity": 46,
        }
        data_before = LoggedData.objects.count()
        result = self.client.post(f"/api/log_data/{self.s1.name}/", data)
        data_after = LoggedData.objects.count()

        assert result.status_code == 201
        assert data_after == data_before + 1

    def test_get_data_for_existing_sensor(self):
        result = self.client.get(f"/api/log_data/{self.s1.name}/")

        assert result.status_code == 200
        assert len(result.data) == 200

    def test_data_for_not_existing_sensor(self):
        result = self.client.get(
            "/api/log_data/ThisSensorNameDoesNotExistInTheDatabase/"
        )

        assert result.status_code == 404


class AllDataTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        add_sensors(cls)
        add_sensor_data(cls)
        return super().setUpTestData()

    def test_get_all_logged_data(self):
        result = self.client.get("/api/log_data/all/")
        assert result.status_code == 200
        assert len(result.data) == 400


class SensorsListTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        add_sensors(cls)
        return super().setUpTestData()

    def test_(self):
        result = self.client.get("/api/sensors_list/")
        assert result.status_code == 200
        assert len(result.data) == 2
