import os

from pathlib import Path
from from_root import from_root
from dataclasses import dataclass

from src.constants import *

@dataclass
class PipelineConfig:
    artifact_folder: Path = os.path.join(from_root(), ARTEFACT_DIR_NAME)
    artifact_dir : Path =  os.path.join(artifact_folder, TIMESTAMP)
    
pipeline_config : PipelineConfig = PipelineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_folder: Path = os.path.join(pipeline_config.artifact_dir, DATA_INGESTION_FOLDER_NAME)
    feature_store_folder: Path = os.path.join(data_ingestion_folder, FEATURE_STORE_FOLDER_NAME)
    ingested_folder: Path = os.path.join(data_ingestion_folder, INGESTED_FOLDER_NAME)
    feature_store_file: Path = os.path.join(feature_store_folder, FEATURE_STORE_FILE_NAME)
    ingested_file = Path = os.path.join(ingested_folder, INGESTED_FILE_NAME)

@dataclass
class DataValidationConfig:
    data_validation_folder: Path = os.path.join(pipeline_config.artifact_dir, DATA_VALIDATION_FOLDER_NAME)
    report_file: Path = os.path.join(data_validation_folder, REPORT_FILE_NAME)

@dataclass
class DataTransformationConfig:
    data_transformation_folder: Path = os.path.join(pipeline_config.artifact_dir, DATA_TRANSFORMATION_FOLDER_NAME)
    train_arr_file_path: Path = os.path.join(data_transformation_folder, TRAIN_ARR_FILE_NAME)
    test_arr_file_path: Path = os.path.join(data_transformation_folder, TEST_ARR_FILE_NAME)