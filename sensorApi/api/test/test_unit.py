from rest_framework.test import APITestCase

from api.models import RegisteredSensors

# Create your tests here.


class SanityTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sensor = RegisteredSensors(name="thisIsAnID", display_name="Test1")
        cls.sensor.save()
        return super().setUpTestData()

    def test_sanity(self):
        sensor = RegisteredSensors.objects.get(pk=self.sensor.pk)
        assert sensor == self.sensor
