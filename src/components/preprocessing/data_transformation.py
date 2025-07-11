import os
import sys
import numpy as np
import pandas as pd

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from src.constants import *
from src.logging import logging
from src.exception import MyException
from src.utils import ultra_json, save_and_load_np_array
from src.components.preprocessing.data_preprocessing import Preprocessing
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import (
    DataIngestionArtifact, 
    DataTransformationArtifact, 
    DataValidationArtifact
)

class DataTransformation:
    def __init__(self):
        try:
            self.preprocessing : Preprocessing = Preprocessing()
        except Exception as e:
            raise MyException(e, sys) from e
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            logging.info('TfidfVectorizer Initialize....')
            tfidf: TfidfVectorizer = TfidfVectorizer(max_features=MAX_FEATURES)
            
            logging.info('Data Preprocessing Started....')
            processed_df: pd.DataFrame = self.preprocessing.preprocess(df)
            logging.info('Data Preprocessing Successful....')
            
            logging.info('Data Spliting Initialize....')
            train, test = train_test_split(processed_df, test_size=TEST_SIZE, random_state=1)
            
            input_feature_train = train['Comment']
            input_feature_test = test['Comment']
            
            target_feature_train = train['Sentiment']
            target_feature_test = test['Sentiment']
            
            logging.info('Data vectorizing Initialized ....')
            vector_train_feature = tfidf.fit_transform(input_feature_train).toarray()
            vector_test_feature = tfidf.transform(input_feature_test).toarray()
            logging.info('Data vectorization successfull....')
            
            train_arr = np.c_[vector_train_feature, np.array(target_feature_train)]
            test_arr = np.c_[vector_test_feature, np.array(target_feature_test)]
            
            return train_arr, test_arr
                      
        except Exception as e:
            raise MyException(e, sys) from e
        
    def data_transformation_initialize(
        self,
        ingested_file_path: DataIngestionArtifact, 
        validation_path: DataValidationArtifact,
        train_arr_save_file_path: DataTransformationConfig,
        test_arr_save_file_path: DataTransformationConfig
    ) -> DataTransformationArtifact:
        try:
            logging.info('Data Transformation Started....')
            logging.info('Verification report loading....')
            status = ultra_json(
                path=validation_path
            )
            logging.info('Successfully loaded the report....')
            
            if status['status'] != True:
                logging.info(f'Data is not Valid: {status['message']}')
            else:
                logging.info('Ingested file loading....')
                ingested_df: pd.DataFrame = pd.read_csv(ingested_file_path)
                logging.info('Successfully loaded the ingested data....')
                
                logging.info('Data Transformation Started....')
                _train_arr, _test_arr = self.transform(ingested_df)
                logging.info('Data Transformation Successful....')
                
                _train_arr_path: Path = Path(train_arr_save_file_path)
                _test_arr_path: Path = Path(test_arr_save_file_path)
                
                _train_arr_path.parent.mkdir(parents=True, exist_ok=True)
                _test_arr_path.parent.mkdir(parents=True, exist_ok=True)
                
                logging.info('Saving Transformed array....')
                save_and_load_np_array(
                    path=_train_arr_path,
                    arr=_train_arr,
                    statement='save'
                )
                
                save_and_load_np_array(
                    path=_test_arr_path,
                    arr=_test_arr,
                    statement='save'
                )
                logging.info('Saving Transformed array is successful....')
                data_transformation_artifact: DataTransformationArtifact = DataTransformationArtifact(
                    train_arr_file_path=_train_arr_path,
                    test_arr_file_path=_test_arr_path
                )
                
                logging.info('Returning Data Transformation Artifact....')
                return data_transformation_artifact
                
        except Exception as e:
            raise MyException(e, sys) from e
    