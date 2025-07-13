import os
import sys
import json
import numpy as np
import pandas as pd

from pathlib import Path
from lightgbm import LGBMClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score
)

from src.logging import logging
from src.exception import MyException
from src.utils import (
    save_and_load_np_array,
    pickler,
    ultra_json
)
from src.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelBuilderArtifact
)
from src.entity.config_entity import ModelBuildConfig



class ModelBuilder:
    def build_model(self, train_df: DataTransformationArtifact) -> LGBMClassifier:
        try:
            logging.info('Loading training data from artifact....')
            _data: np.array = save_and_load_np_array(
                path=train_df
            )
            logging.info(f'Loading Successful from -> {train_df}')

            logging.info('Splitting data into X_train, y_train....')
            X_train = _data[:, :-1]
            y_train = _data[:, -1]
            logging.info('Splitting Successful....')

            logging.info('Model Initialize....')
            model = LGBMClassifier()

            logging.info('Training Started....')
            model.fit(X_train,y_train)
            logging.info(f'Training Successful -> {model}')

            return model
            
        except Exception as e:
            raise MyException(e, sys) from e

    def performance_matrix(self, model: LGBMClassifier, test_df: DataTransformationArtifact) -> json:
        try:
            logging.info('Loading test data from artifact....')
            _data: np.array = save_and_load_np_array(
                path=test_df
            )
            logging.info(f'Loading Successful from -> {test_df}')

            logging.info('Splitting data into X_test, y_test....')
            X_test = _data[:, :-1]
            y_test = _data[:, -1]
            logging.info('Splitting Successful....')

            logging.info('Matrix Calculation Started....')
            y_pred = model.predict(X_test)

            matrix = {
                'accuracy_score' : accuracy_score(y_test, y_pred),
                'f1_score' : f1_score(y_test, y_pred, average='micro'),
                'precision_score' : precision_score(y_test, y_pred, average='micro'),
                'recall_score' : recall_score(y_test, y_pred, average='micro')
            }
            logging.info(f'Matrix Calculation successful --> {matrix}')
            return matrix
        except Exception as e:
            raise MyException(e, sys) from e
        
    def model_builder_initialize(
            self,
            train_df: DataTransformationArtifact,
            test_df: DataTransformationArtifact,
            model_file: ModelBuildConfig,
            matrix_file: ModelBuildConfig
    ) -> ModelBuilderArtifact:
        try:
            logging.info('Model Building Started....')
            model = self.build_model(
                train_df=train_df
            )

            matrix = self.performance_matrix(
                model=model,
                test_df=test_df
            )

            model_file_path: Path = Path(model_file)
            model_file_path.parent.mkdir(parents=True, exist_ok=True)

            pickler(
                model=model,
                file_path=model_file_path,
                statement='dump'
            )

            matrix_file_path: Path = Path(matrix_file)
            matrix_file_path.parent.mkdir(parents=True, exist_ok=True)

            ultra_json(
                path=matrix_file_path,
                data=matrix,
                statement='create'
            )

            model_builder_artifact: ModelBuilderArtifact = ModelBuilderArtifact(
                model_file=model_file_path,
                matrix_file=matrix_file_path
            )

            logging.info('Model Building Successful....')

            return model_builder_artifact
        except Exception as e:
            raise MyException(e, sys) from e
