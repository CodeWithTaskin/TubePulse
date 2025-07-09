import os
import sys
import yaml
import json

from pathlib import Path
from src.logging import logging
from src.exception import MyException


def load_yaml(path: Path) -> yaml:
    try:
        with open(path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except Exception as e:
        raise MyException(e, sys) from e
    
def ultra_json(path: Path, data: json = None, statement: str = 'load') -> json:
    try:
        if statement == 'create':
            with open(path, "w") as json_file:
                json.dump(data, json_file, indent=4)
            logging.info(f"JSON data successfully written to {path}")
            
        elif statement == 'load':
            with open(path, 'r') as file:
                config_data = json.load(file)
                
            logging.info('JSON data successfully loaded....')
            return config_data
        
        else:
            raise logging.info('Invalid Statement....')
    except Exception as e:
        raise MyException(e, sys) from e