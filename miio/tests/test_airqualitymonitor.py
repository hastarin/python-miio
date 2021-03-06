from unittest import TestCase
from miio import AirQualityMonitor
from .dummies import DummyDevice
import pytest


class DummyAirQualityMonitor(DummyDevice, AirQualityMonitor):
    def __init__(self, *args, **kwargs):
        self.state = {
            'power': 'on',
            'aqi': 34,
            'battery': 100,
            'usb_state': 'off'
        }
        self.return_values = {
            'get_prop': self._get_state,
            'set_power': lambda x: self._set_state("power", x),
        }
        super().__init__(args, kwargs)


@pytest.fixture(scope="class")
def airqualitymonitor(request):
    request.cls.device = DummyAirQualityMonitor()
    # TODO add ability to test on a real device


@pytest.mark.usefixtures("airqualitymonitor")
class TestAirQualityMonitor(TestCase):
    def is_on(self):
        return self.device.status().is_on

    def state(self):
        return self.device.status()

    def test_on(self):
        self.device.off()  # ensure off

        start_state = self.is_on()
        assert start_state is False

        self.device.on()
        assert self.is_on() is True

    def test_off(self):
        self.device.on()  # ensure on

        assert self.is_on() is True
        self.device.off()
        assert self.is_on() is False

    def test_status(self):
        self.device._reset_state()

        assert self.is_on() is True
        assert self.state().aqi == self.device.start_state["aqi"]
        assert self.state().battery == self.device.start_state["battery"]
        assert self.state().usb_power == (self.device.start_state["usb_state"] == 'on')
