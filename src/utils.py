import os
import time
import json
from typing import Union, List, Dict, Optional

import yaml
import requests
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


def json_dump(filename: str, data: Union[List, Dict]) -> None:
    """Dump data to json format and save to file"""

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f)


def json_load(filename: str) -> Union[List, Dict]:
    """Load json data from file"""

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def load_configuration(config_file: str) -> Dict:
    """Load configuration from yaml file"""

    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def get_db_connection_engine(
    user: str = os.getenv("PG_USER"),
    pwd: str = os.getenv("PG_PASSWORD"),
    database: str = os.getenv("PG_DB"),
    host: str = os.getenv("PG_HOST"),
    port: str = os.getenv("PG_PORT"),
) -> Engine:
    """Create database connection engine"""

    conn_string = (
        f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{database}"
    )

    return create_engine(conn_string)


def make_request(
    url: str, headers: Dict, max_retries: int = 5
) -> Optional[Dict]:
    for retry in range(max_retries):
        resp = requests.get(url, headers=headers)
        if resp.ok:
            return resp.json()
        else:
            print(f"{url} retry {retry}")
            time.sleep(0.5)
    return None
