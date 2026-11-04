from typing import Any


def parse_config(filename: str) -> dict[str, Any]:
    """Read and validate a maze configuration file.

    The file must contain one KEY=VALUE pair per line. Empty lines and
    lines starting with '#' are ignored.

    Args:
        filename: path of the configuration file.

    Returns:
        A dictionary with the converted values: WIDTH and HEIGHT (int),
        ENTRY and EXIT (tuple of two ints), OUTPUT_FILE (str), PERFECT
        (bool) and, if present, SEED (int).

    Raises:
        OSError: if the file cannot be read.
        ValueError: if a line is malformed, a key is missing or a value
            is invalid.
    """

    config: dict[str, Any] = {}

    with open(filename) as f:
        for line in f:
            line = line.strip()

            if line == "" or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(f"line without '=': {line}")

            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

    required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    for key in required:
        if key not in config:
            raise ValueError(f"Key is missing: {key}")

    try:
        config["WIDTH"] = int(config["WIDTH"])
    except ValueError:
        raise ValueError("WIDTH must be integer")

    try:
        config["HEIGHT"] = int(config["HEIGHT"])
    except ValueError:
        raise ValueError("HEIGHT must be integer")

    if config["WIDTH"] <= 0 or config["HEIGHT"] <= 0:
        raise ValueError("The WIDTH and the HEIGHT must be bigger than 0")

    try:
        config["ENTRY"] = tuple(map(int, config["ENTRY"].split(",", 1)))
    except ValueError:
        raise ValueError("The ENTRY must be a tuple of integers")

    try:
        config["EXIT"] = tuple(map(int, config["EXIT"].split(",", 1)))
    except ValueError:
        raise ValueError("The EXIT must be a tuple of integers")

    if len(config["ENTRY"]) != 2 or len(config["EXIT"]) != 2:
        raise ValueError("The ENTRY and the EXIT must be 2 elements")

    if config["OUTPUT_FILE"] == "":
        raise ValueError("The OUTPUT_FILE must have a name")

    if config["PERFECT"] == "True":
        config["PERFECT"] = True
    elif config["PERFECT"] == "False":
        config["PERFECT"] = False
    else:
        raise ValueError("PERFECT must be 'True' or 'False'")

    if "SEED" in config:
        try:
            config["SEED"] = int(config["SEED"])
        except ValueError:
            raise ValueError("SEED must be integer")

    for name, point in (("ENTRY", config["ENTRY"]), ("EXIT", config["EXIT"])):
        x, y = point
        if not 0 <= x < config["WIDTH"] or not 0 <= y < config["HEIGHT"]:
            raise ValueError(f"{name} is outside the maze")

    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("ENTRY and EXIT must be different")

    return config
