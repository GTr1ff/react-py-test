import logging
import logging.config
import sys
from pathlib import Path
from core.config import settings
from core.logging.data_filter import SensitiveDataLoggingFilter

def setup_logging() -> None:
    """Configure logging for the application"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(exist_ok=True)

    sensitive_data_filter = "sensitive_data_filter"
    timed_rotating_file_handler = "logging.handlers.TimedRotatingFileHandler"
    
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "format": '{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "message": "%(message)s", "module": "%(module)s", "function": "%(funcName)s", "line": %(lineno)d}',
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
         "filters": {
            "sensitive_data_filter": {
                "()": SensitiveDataLoggingFilter,
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.LOG_LEVEL,
                "formatter": "default",
                "filters": [] if settings.DEBUG else [sensitive_data_filter],
                "stream": sys.stdout,
            },
            "file": {
                "class": timed_rotating_file_handler,
                "level": settings.LOG_LEVEL,
                "formatter": "json",
                "filters": [] if settings.DEBUG else [sensitive_data_filter],
                "filename": f"{log_dir}/app.ndjson.log",
                "when": "midnight",
                "interval": 1,
                "backupCount": 7,
            },
            "repository_file": {
                "class": timed_rotating_file_handler,
                "level": settings.LOG_LEVEL,
                "formatter": "json",
                "filters": [] if settings.DEBUG else [sensitive_data_filter],
                "filename": f"{log_dir}/repository.ndjson.log",
                "when": "midnight",
                "interval": 1,
                "backupCount": 7,
            },
            "error_file": {
                "class": timed_rotating_file_handler,
                "level": "ERROR",
                "formatter": "json",
                "filters": [] if settings.DEBUG else [sensitive_data_filter],
                "filename": f"{log_dir}/error.ndjson.log",
                "when": "midnight",
                "interval": 1,
                "backupCount": 7,
            }
        },
        "loggers": {
            "app": {  
                "level": settings.LOG_LEVEL,
                "handlers": ["console", "file", "error_file"],
                "propagate": False,
            },
            "app.repository": {  
                "level": settings.LOG_LEVEL,
                "handlers": ["console", "repository_file", "error_file"],
                "propagate": False,
            },
            "features": { 
                "level": settings.LOG_LEVEL,
                "handlers": ["console", "file", "error_file"],
                "propagate": False,
            },
            
        }
    }
    
    logging.config.dictConfig(logging_config)