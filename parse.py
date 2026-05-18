import sys


def validator(argv: list[str]):
    if len(argv) < 2 or len(argv) > 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    if argv[1] != "config.txt":
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)


def read_config(file_path) -> dict:
    config = {}
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, value = line.split('=', 1)
            config[key.strip()] = value.strip()
    return config


def parse_coordinates(value: str) -> tuple[(int, int)]:
    x, y = value.split(',')
    return int(x), int(y)


def parse_config(config: dict):
    parsed = {}
    config_report = []

    try:
        parsed['WIDTH'] = int(config['WIDTH'])
    except ValueError:
        config_report.append("WIDTH - invalid parameter")

    try:
        parsed['HEIGHT'] = int(config['HEIGHT'])
    except ValueError:
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
        parsed['PERFECT"'] = config["PERFECT"] == "True"
    except ValueError:
        config_report.append("PERFECT - invalid parameter")

    if config_report:
        config_report.append("==== CONFIG.TXT BAD VALUES REPORT ====\n")
        for error in config_report:
            print(f"{error}")
        sys.exit(1)
    else:
        return parsed
