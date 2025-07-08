import os
import sys
import yaml

from pathlib import Path
from src.exception import MyException


def load_yaml(path: Path) -> yaml:
    try:
        with open(path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except Exception as e:
        raise MyException(e, sys) from e