#!/usr/bin/env python3
"""Convert temperature between Celsius and Fahrenheit."""
import argparse


class TemperatureConverter:
    def __init__(self, temperature: float, unit: str):
        """Initializes a new instance of the TemperatureConverter class.

        Args:
            temperature (float): The temperature value to be converted.
            unit (str): The unit of temperature to be converted, either Celsius (C) or Fahrenheit (F).
        """
        self.temperature = temperature
        self.unit = unit

    def to_celsius(self) -> float:
        """Converts a temperature from Fahrenheit to Celsius.

        Returns:
            float: The temperature in Celsius.
        """
        if self.unit == "F":
            return (self.temperature - 32) * 5 / 9
        else:
            return self.temperature

    def to_fahrenheit(self) -> float:
        """Converts a temperature from Celsius to Fahrenheit.

        Returns:
            float: The temperature in Fahrenheit.
        """
        if self.unit == "C":
            return self.temperature * 9 / 5 + 32
        else:
            return self.temperature


def parse_args() -> argparse.Namespace:
    """Parses command line arguments.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Convert temperature from Celsius to Fahrenheit or vice versa."
    )
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        help="Temperature value to be converted.",
        required=True,
    )
    parser.add_argument(
        "-u",
        "--unit",
        type=str,
        choices=["C", "F"],
        help="Unit of temperature to be converted, either Celsius (C) or Fahrenheit (F).",
        required=True,
    )
    try:
        return parser.parse_args()
    except SystemExit:
        parser.print_help()
        exit()


if __name__ == "__main__":
    args = parse_args()

    temp_converter = TemperatureConverter(args.temperature, args.unit)

    if args.unit == "C":
        converted_temp = temp_converter.to_fahrenheit()
        print(f"{args.temperature:.2f}°C = {converted_temp:.2f}°F")
    elif args.unit == "F":
        converted_temp = temp_converter.to_celsius()
        print(f"{args.temperature:.2f}°F = {converted_temp:.2f}°C")
