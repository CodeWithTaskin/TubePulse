import os
import sys
import csv
import pandas as pd

from pathlib import Path
from from_root import from_root

from src.constants import *
from src.logging import logging
from src.utils import load_yaml
from src.exception import MyException
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.configuration.mongodb.mongo_db_connection import MongoDBConnection

class DataIngestion:
    def __init__(self):
        try:
            self.mongodb_connection: MongoDBConnection = MongoDBConnection(
                db_name=DB_NAME,
                collection_name=COLLECTION_NAME,
                connection_url=os.getenv(CONNECTION_URL)
            )
        except Exception as e:
            raise MyException(e, sys) from e
        
    def data_collection_and_export_csv(self, feature_store_path: DataIngestionConfig) -> Path:
        try:
            logging.info('Data Collection Started....')
            documents = self.mongodb_connection.collection_entity().find()
            
            first_doc = documents.next()
            fieldnames = first_doc.keys()

            logging.info('Ingestion path defined....')
            feature_store: Path = Path(feature_store_path)
            feature_store.parent.mkdir(parents=True,exist_ok=True)
            
            logging.info('Start saving as csv file....')
            with open(feature_store, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()

                writer.writerow(first_doc)
                for doc in documents:
                    writer.writerow(doc)
                    
            logging.info('Successfully saving csv file....')
            return feature_store
        
        except Exception as e:
            raise MyException(e, sys) from e

    def remove_unnecessary_columns_and_export_csv(self, feature_store_path: DataIngestionConfig, ingested_path: DataIngestionConfig) -> Path:
        try:
            logging.info('Loading csv from feature store folder....')
            df: pd.DataFrame = pd.read_csv(feature_store_path)
            
            logging.info('Loading schema.yaml from config folder....')
            schema = load_yaml(os.path.join(from_root(), 'config', 'schema.yaml'))
            
            if schema['unnecessary_col'][0] in df.columns:
                df: pd.DataFrame = df.drop(columns=schema['unnecessary_col'])
            
            ingestion_file_path: Path = Path(ingested_path)
            ingestion_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            logging.info('Saving clean data into ingestion folder....')
            df.to_csv(ingestion_file_path, index=False)
            return ingestion_file_path
        
        except Exception as e:
            raise MyException(e, sys) from e
        
    def data_ingestion_initialize(self, feature_store_path: DataIngestionConfig, ingested_path: DataIngestionConfig) -> DataIngestionArtifact:
        try:
            data_collection = self.data_collection_and_export_csv(
                feature_store_path=feature_store_path
            )
            
            drop_unnecessary_col = self.remove_unnecessary_columns_and_export_csv(
                feature_store_path=data_collection,
                ingested_path=ingested_path
            )
            
            data_ingestion_artifact: DataIngestionArtifact = DataIngestionArtifact(
                ingestion_file=drop_unnecessary_col
            )
            
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e, sys) from e