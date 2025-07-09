from datetime import datetime


ARTEFACT_DIR_NAME: str = 'artefact'
TIMESTAMP: str = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
LOG_DIR = 'logs'
LOG_FILE = f'{TIMESTAMP}.log'
MAX_LOG_SIZE = 5 * 1024 * 1024 #5 MB
BACKUP_COUNT = 3 #Number of backup log to keep

# MongoDB configuration Constants
DB_NAME: str = 'TubePulse'
COLLECTION_NAME: str = 'TubePulse_Data'
CONNECTION_URL: str = 'MONGODB_URL'

# Data Ingestion Constants starts from DATA_INGESTION_FOLDER_NAME variable
DATA_INGESTION_FOLDER_NAME: str = 'Data_Ingestion'
FEATURE_STORE_FOLDER_NAME: str = 'feature_store'
FEATURE_STORE_FILE_NAME: str = 'data.csv'
INGESTED_FOLDER_NAME: str = 'ingested'
INGESTED_FILE_NAME: str = 'clean_data.csv'

# Data Validation Constants starts from DATA_VALIDATION_FOLDER_NAME variable
DATA_VALIDATION_FOLDER_NAME: str = 'Data_Validation'
REPORT_FILE_NAME: str = 'report.json'






