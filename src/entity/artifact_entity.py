from pathlib import Path
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    ingestion_file: Path

@dataclass
class DataValidationArtifact:
    report_file_path: Path
    
@dataclass
class DataTransformationArtifact:
    train_arr_file_path: Path
    test_arr_file_path: Path

@dataclass
class ModelBuilderArtifact:
    model_file: Path
    matrix_file: Path