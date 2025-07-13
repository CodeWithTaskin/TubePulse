import os
import sys
import json
import pandas as pd

from pathlib import Path
from from_root import from_root

from src.logging import logging
from src.utils import ultra_json, load_yaml
from src.exception import MyException
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataValidationConfig

class DataValidation:
    def status(self, ingested_file: DataIngestionArtifact) -> bool:
        try:
            schema = load_yaml(os.path.join(from_root(), 'config', 'schema.yaml'))
            ingested_df: pd.DataFrame = pd.read_csv(ingested_file)
            
            arg = schema['columns'] == ingested_df.columns
            if arg.all():
                return True
            
            else:
                return False
            
        except Exception as e:
            raise MyException(e, sys) from e
    
    
    def data_validation_initialize(self, ingested_file: DataIngestionArtifact, report_file_path: DataValidationConfig) -> DataValidationArtifact:
        try:
            message = ''
            status = ''
            
            logging.info('Start Data Validation....')
            check_status = self.status(ingested_file=ingested_file)
            
            logging.info('Checking Status....')
            if check_status:
                status = check_status
            else:
                message = 'Column is not match'
                status = check_status
            
            logging.info('Report initialize....')    
            report = {
                'message' : message,
                'status' : status
            }
            
            logging.info('Report file path initialize....')
            report_file = Path(report_file_path)
            report_file.parent.mkdir(parents=True,exist_ok=True)
            
            logging.info('Saving report....')
            make_report = ultra_json(
                path=report_file_path,
                data=report,
                statement='create'
            )
            
            logging.info('Saving report file path on artifact....')
            data_validation_artifact: DataValidationArtifact = DataValidationArtifact(
                report_file_path=report_file
            )
            
            logging.info('Data Validation Successful....')
            return data_validation_artifact
        except Exception as e:
            raise MyException(e, sys) from e