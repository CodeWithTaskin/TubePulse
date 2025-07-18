import os
import sys
import yaml
import gzip
import json
import joblib
import numpy as np

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
    
def save_and_load_np_array(path: Path, arr: np.array = None, statement = 'load') -> np.array:
    try:
        if statement == 'save':
            with gzip.GzipFile(path, "w") as f:
                np.save(f, arr)
        elif statement == 'load':
            with gzip.GzipFile(path, "r") as f:
                loaded_data = np.load(f, allow_pickle=True)
            return loaded_data
        else:
            logging.info('Invalid statement....')
    except Exception as e:
        raise MyException(e, sys) from e
    
def pickler(file_path: Path, model=None, statement = 'load'):
    try:
        if statement == 'dump':
            joblib.dump(value=model, filename=file_path, compress=True)
        elif statement == 'load':
            loaded_file = joblib.load(filename=file_path)
            return loaded_file
        else:
            logging.info('Invalid statement....')
    except Exception as e:
        raise MyException(e, sys) from e