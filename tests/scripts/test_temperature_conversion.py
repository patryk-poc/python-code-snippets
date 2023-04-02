import pytest

from tools.scripts.convert_temperature import TemperatureConverter


class TestTemperatureConverter:
    @pytest.mark.parametrize(
        "celsius_temp, expected_fahrenheit", [(0, 32), (-40, -40), (100, 212)]
    )
    def test_celsius_to_fahrenheit(self, celsius_temp, expected_fahrenheit):
        converter = TemperatureConverter(celsius_temp, "C")
        assert converter.to_fahrenheit() == expected_fahrenheit

    @pytest.mark.parametrize(
        "fahrenheit_temp, expected_celsius", [(32, 0), (-40, -40), (212, 100)]
    )
    def test_fahrenheit_to_celsius(self, fahrenheit_temp, expected_celsius):
        converter = TemperatureConverter(fahrenheit_temp, "F")
        assert converter.to_celsius() == expected_celsius
