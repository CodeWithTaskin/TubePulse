from src.components.ingestion.data_ingestion import DataIngestion
from src.components.validation.data_validation import DataValidation
from src.components.preprocessing.data_transformation import DataTransformation
from src.components.model.model_bulding import ModelBuilder


from src.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelBuildConfig
)

from src.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelBuilderArtifact
)


class Pipeline:
    def __init__(self):
        self.data_ingestion_config: DataIngestionConfig = DataIngestionConfig()
        self.data_validation_config: DataValidationConfig = DataValidationConfig()
        self.data_transformation_config: DataTransformationConfig = DataTransformationConfig()
        self.model_builder_config: ModelBuildConfig = ModelBuildConfig()
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        data_ingestion: DataIngestion = DataIngestion()
        
        data_ingestion_initialize = data_ingestion.data_ingestion_initialize(
            feature_store_path=self.data_ingestion_config.feature_store_file,
            ingested_path=self.data_ingestion_config.ingested_file
        )
        
        return data_ingestion_initialize
    
    def start_data_validation(self, ingested_file: DataIngestionArtifact) -> DataValidationArtifact:
        data_validation: DataValidation = DataValidation()
        
        data_validation_initialize = data_validation.data_validation_initialize(
            ingested_file=ingested_file,
            report_file_path=self.data_validation_config.report_file
        )
        
        return data_validation_initialize
    
    def start_data_transformation(
        self, 
        ingested_file: DataIngestionArtifact, 
        validation_report: DataValidationArtifact
    ) -> DataTransformationArtifact:
        data_transformation: DataTransformation = DataTransformation()
        
        data_transformation_initialize = data_transformation.data_transformation_initialize(
            ingested_file_path=ingested_file,
            validation_path=validation_report,
            train_arr_save_file_path=self.data_transformation_config.train_arr_file_path,
            test_arr_save_file_path=self.data_transformation_config.test_arr_file_path
        )
        
        return data_transformation_initialize
    
    def start_model_building(
        self,
        train_df: DataTransformationArtifact,
        test_df: DataTransformationArtifact
    ) -> ModelBuilderArtifact:
        model_builder: ModelBuilder = ModelBuilder()

        model_builder_initialize = model_builder.model_builder_initialize(
            train_df=train_df,
            test_df=test_df,
            model_file=self.model_builder_config.model_file,
            matrix_file=self.model_builder_config.matrix_file
        )

        return model_builder_initialize
        
    
    def run_pipeline(self):
        data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()
        data_validation_artifact: DataValidationArtifact = self.start_data_validation(
            ingested_file=data_ingestion_artifact.ingestion_file
        )
        
        data_transformation_artifact: DataTransformationArtifact = self.start_data_transformation(
            ingested_file=data_ingestion_artifact.ingestion_file,
            validation_report=data_validation_artifact.report_file_path
        )

        model_builder_artifact: ModelBuilderArtifact = self.start_model_building(
            train_df=data_transformation_artifact.train_arr_file_path,
            test_df=data_transformation_artifact.test_arr_file_path
        )