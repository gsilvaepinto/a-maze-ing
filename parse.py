from __future__ import annotations
import sys
from typing import Any


class ParsingError(Exception):
    """Raised when a config value is present but invalid."""

    def __init__(self, message: str = "") -> None:
        """Initialize with an optional error message."""
        super().__init__(message)


class OutOffBound(Exception):
    """Raised when coordinates fall outside maze boundaries."""

    def __init__(self, message: str = "") -> None:
        """Initialize with an optional error message."""
        super().__init__(message)


def validator(argv: list[str]) -> None:
    """Validate that exactly one command-line argument was provided."""
    if len(argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)


def read_config(file_path: str) -> dict[str, str]:
    """Read a KEY=VALUE config file and return a raw string dict.

    Args:
        file_path: Path to the configuration file.

    Returns:
        Dict mapping each key to its raw string value.
    """
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
        print("Error: Config file not found")
        sys.exit(1)
    except ValueError:
        print("Error: wrong file format")
        sys.exit(1)

    return config


def parse_coordinates(value: str) -> tuple[int, int]:
    """Parse a 'x,y' string into a tuple of ints."""
    x, y = value.split(',')
    return int(x), int(y)


def out_of_boundaries(height: int,
                      width: int,
                      entry: tuple[int, int],
                      exit: tuple[int, int],
                      config_report: list[str]) -> list[str]:
    """Append errors to config_report if entry or exit are outside maze bounds.

    Args:
        height: Maze height in cells.
        width: Maze width in cells.
        entry: Entry coordinates (x, y).
        exit: Exit coordinates (x, y).
        config_report: Accumulator list for error messages.

    Returns:
        The updated config_report list.
    """
    ex, ey = entry
    xx, xy = exit

    if not (0 <= ex < width and 0 <= ey < height):
        config_report.append(f"Error: ENTRY {entry} is out of boundaries for"
                             f" maze {width}x{height}")

    if not (0 <= xx < width and 0 <= xy < height):
        config_report.append(f"Error: EXIT {exit} is out of boundaries for"
                             f" maze {width}x{height}")

    if entry == exit:
        config_report.append("Error: ENTRY and EXIT must be different cells")

    return config_report


def parse_config(config: dict[str, str]) -> dict[str, Any]:
    """Validate and convert the raw config dict into typed values.

    Args:
        config: Raw string dict from read_config.

    Returns:
        Dict with typed values for WIDTH, HEIGHT, ENTRY, EXIT,
        OUTPUT_FILE, and PERFECT.
    """
    parsed: dict[str, Any] = {}
    config_report: list[str] = []

    try:
        parsed['WIDTH'] = int(config['WIDTH'])
        if parsed['WIDTH'] <= 0:
            raise ParsingError()
    except (ValueError, ParsingError):
        config_report.append("WIDTH - invalid parameter")
    except KeyError:
        config_report.append("WIDTH - missing parameter")

    try:
        parsed['HEIGHT'] = int(config['HEIGHT'])
        if parsed['HEIGHT'] <= 0:
            raise ParsingError(("HEIGHT - invalid parameter height cant be 0"
                                " or negative"))
    except (ValueError, ParsingError):
        config_report.append("HEIGHT - invalid parameter")
    except KeyError:
        config_report.append("HEIGHT - missing parameter")

    try:
        parsed['ENTRY'] = parse_coordinates(config['ENTRY'])
    except (ValueError):
        config_report.append("ENTRY - invalid parameter")
    except KeyError:
        config_report.append("ENTRY - missing parameter")

    try:
        parsed['EXIT'] = parse_coordinates(config['EXIT'])
    except (ValueError):
        config_report.append("EXIT - invalid parameter")
    except KeyError:
        config_report.append("EXIT - missing parameter")

    try:
        parsed['OUTPUT_FILE'] = config["OUTPUT_FILE"]
    except ValueError:
        config_report.append("OUTPUT_FILE - invalid parameter")
    except KeyError:
        config_report.append("OUTPUT_FILE - missing parameter")

    try:
        if config['PERFECT'] not in ("True", "False"):
            raise ParsingError("PERFECT - invalid parameter")
        parsed['PERFECT'] = config['PERFECT'] == "True"
    except (ValueError, ParsingError):
        config_report.append("PERFECT - invalid parameter")
    except KeyError:
        config_report.append("PERFECT - missing parameter")

    if not config_report:
        config_report = out_of_boundaries(parsed['HEIGHT'], parsed['WIDTH'],
                                          parsed['ENTRY'], parsed['EXIT'],
                                          config_report)

    if config_report:
        print("WARNING: UNABLE TO REPRODUCE THE MAZE")
        print("==== CONFIG.TXT INVALID PARAMETERS REPORT ====\n")
        for error in config_report:
            print(f"{error}")
        sys.exit(1)
    else:
        return parsed
