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


def parse_coordinates(value: str) -> tuple[int, int]:
    x, y = value.split(',')
    return int(x), int(y)


def parse_config(config: dict) -> dict:
    parsed = {}

    parsed['WIDTH'] = int(config['WIDTH'])
    parsed['HEIGHT'] = int(config['HEIGHT'])
    parsed['ENTRY'] = parse_coordinates(config['ENTRY'])
    parsed['EXIT'] = parse_coordinates(config['EXIT'])
    parsed["OUTPUT_FILE"] = config["OUTPUT_FILE"]
    parsed["PERFECT"] = config["PERFECT"] == "True"

    return parsed
