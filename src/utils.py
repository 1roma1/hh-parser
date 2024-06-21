import json
import yaml
from typing import Union, List, Dict


def json_dump(filename: str, data: Union[List, Dict]):
    """Dump data to json format and save to file"""

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f)


def json_load(filename: str):
    """Load json data from file"""

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def load_configuration(config_file: str) -> Dict:
    """Load configuration from yaml file"""

    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config
