from src.components.ingestion.data_ingestion import DataIngestion


from src.entity.config_entity import (
    DataIngestionConfig
)

from src.entity.artifact_entity import (
    DataIngestionArtifact
)


class Pipeline:
    def __init__(self):
        self.data_ingestion_config: DataIngestionConfig = DataIngestionConfig()
    
    def start_data_ingestion(self):
        data_ingestion: DataIngestion = DataIngestion()
        
        data_ingestion_initialize = data_ingestion.data_ingestion_initialize(
            feature_store_path=self.data_ingestion_config.feature_store_file,
            ingested_path=self.data_ingestion_config.ingested_file
        )
        
        return data_ingestion_initialize
    
    def run_pipeline(self):
        data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()