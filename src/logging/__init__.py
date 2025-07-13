import logging
import os
from logging.handlers import RotatingFileHandler
from from_root import from_root
from src.constants import LOG_DIR, LOG_FILE, MAX_LOG_SIZE, BACKUP_COUNT

# Construct full log file path
log_dir_path = os.path.join(from_root(), LOG_DIR)
os.makedirs(log_dir_path, exist_ok=True)
log_file_path = os.path.join(log_dir_path, LOG_FILE)

def configure_logger():
    """
    Configures the root logger with a rotating file handler and console handler.
    Prevents duplicate handlers on re-imports.
    """
    logger = logging.getLogger()  # ✅ Root logger to capture all logs
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Log format
    formatter = logging.Formatter('[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s')

    # Rotating file handler
    file_handler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Add both handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Call this once at the app entry point
configure_logger()
