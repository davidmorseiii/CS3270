import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name='weather_analysis', log_level=logging.INFO):
    """
    Configure and return a logger with file and console handlers
    Args:
        name: Logger name
        log_level: Logging level
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # don't want duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    # make logs directory if it doesnt exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except OSError as e:
            # if that fails, just use console logging
            print(f"Warning: Could not create log directory: {e}")
            log_dir = None

    # format for log messages
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # file handler with rotation - 10 MB max, keeps 5 backups
    if log_dir:
        try:
            log_file = os.path.join(log_dir, f'{name}.log')
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,
                backupCount=5
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not create file handler: {e}")

    return logger