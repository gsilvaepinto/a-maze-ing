from __future__ import annotations

import sys
from typing import Any


class ParsingError(Exception):
    def __init__(self, message="") -> None:
        super().__init__(message)


def validator(argv: list[str]) -> None:
    if len(argv) < 2 or len(argv) > 2 and argv[1] != "config.txt":
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)


def read_config(file_path: str) -> dict[str, str]:
    config: dict[str, str] = {}
    try:
        with open(file_path) as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    except FileNotFoundError:
        print("Error")
        sys.exit(1)

    return config


def parse_coordinates(value: str) -> tuple[int, int]:
    x, y = value.split(',')
    return int(x), int(y)


def parse_config(config: dict[str, str]) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    config_report: list[str] = []

    try:
        parsed['WIDTH'] = int(config['WIDTH'])
        if parsed['WIDTH'] <= 0:
            raise ParsingError("WIDTH - invalid parameter width cant be 0 or"
                               " negative")
    except (ValueError, ParsingError):
        config_report.append("WIDTH - invalid parameter")

    try:
        parsed['HEIGHT'] = int(config['HEIGHT'])
        if parsed['HEIGHT'] <= 0:
            raise ParsingError(("HEIGTH - invalid parameter height cant be 0"
                                " or negative"))
    except (ValueError, ParsingError):
        config_report.append("HEIGHT - invalid parameter")

    try:
        parsed['ENTRY'] = parse_coordinates(config['ENTRY'])
    except ValueError:
        config_report.append("ENTRY - invalid parameter")

    try:
        parsed['EXIT'] = parse_coordinates(config['EXIT'])
    except ValueError:
        config_report.append("EXIT - invalid parameter")

    try:
        parsed['OUTPUT_FILE'] = config["OUTPUT_FILE"]
    except ValueError:
        config_report.append("OUTPUT_FILE - invalid parameter")

    try:
        parsed['PERFECT'] = config['PERFECT'] == "True"
    except ValueError:
        config_report.append("PERFECT - invalid parameter")

    if config_report:
        print("ERROR: UNABLE TO REPRODUCE THE MAZE")
        print("==== CONFIG.TXT INVALID PARAMETERS REPORT ====\n")
        for error in config_report:
            print(f"{error}")
        sys.exit(1)
    else:
        return parsed
