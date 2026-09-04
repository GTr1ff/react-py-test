import logging
import logging.config
import sys
from pathlib import Path
from core.config import settings
from core.logging.data_filter import SensitiveDataLoggingFilter

def setup_logging() -> None:
    """Configure logging for the application"""
    sensitive_data_filter = "sensitive_data_filter"
    
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
        },
        "loggers": {
            "app": {  
                "level": settings.LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
            "app.repository": {  
                "level": settings.LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
            "features": { 
                "level": settings.LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
            
        }
    }
    
    logging.config.dictConfig(logging_config)