from pathlib import Path
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    ingestion_file: Path
    