import csv
import os
from contextlib import contextmanager
from .logger_config import setup_logger

logger = setup_logger(__name__)

# had to relearn context managers, but I think it will be worth it and is needed for this project
@contextmanager
def open_csv_file(file_path, mode='r', encoding='utf-8'):
    """
    Context manager to safely open and clos CSV files
    Args:
        file_path: Path to the CSV file
        mode: File mode
        encoding: File encoding
    Yields:
        File handle
    Raises:
        FileNotFoundError: File doesn't exist
        PermissionError: Lacking permission to access file
        IOError: Other file I/O errors
    """
    file_handle = None
    try:
        logger.debug(f"Opening file: {file_path}")
        file_handle = open(file_path, mode=mode, encoding=encoding, newline='')
        yield file_handle
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except PermissionError:
        logger.error(f"Permission denied when accessing: {file_path}")
        raise
    except IOError as e:
        logger.error(f"I/O error occurred while accessing {file_path}: {e}")
        raise
    finally:
        if file_handle:
            try:
                file_handle.close()
                logger.debug(f"Closed file: {file_path}")
            except Exception as e:
                logger.warning(f"Error closing file {file_path}: {e}")


def csv_row_generator(file_path):
    """
    Generator to yield rows from CSV file one at a time and memory-efficient for large files
    Args:
        file_path: Path the CSV file
    Yields:
        Dictionary representing each row
    Raises:
        FileNotFoundError: File doesn't exist
        ValueError: CSV file is empty or messed up
        csv.Error: CSV parsing errors
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open_csv_file(file_path) as csvfile:
            reader = csv.DictReader(csvfile)

            # check if file headers
            if reader.fieldnames is None:
                logger.error(f"CSV file has no headers: {file_path}")
                raise ValueError("CSV file has no headers")

            logger.info(f"Reading CSV file: {file_path}")
            logger.debug(f"CSV columns: {reader.fieldnames}")

            row_count = 0
            for row_num, row in enumerate(reader, start=2):  # start at 2, after header
                try:
                    # convert num strings to appropriate types
                    processed_row = {}
                    for key, value in row.items():
                        if value == '' or value is None:
                            processed_row[key] = None
                        else:
                            # try to convert to float if possible
                            try:
                                processed_row[key] = float(value)
                            except (ValueError, TypeError):
                                # keep as string if not number
                                processed_row[key] = value

                    row_count += 1
                    yield processed_row

                except Exception as e:
                    logger.warning(f"Error processing row {row_num}: {e}")
                    # continue processing other rows
                    continue

            if row_count == 0:
                logger.error(f"CSV file is emtpy or has no data rows: {file_path}")
                raise ValueError("CSV file is empty or has no data rows")

            logger.info(f"Successfully read {row_count} rows from {file_path}")

    except csv.Error as e:
        logger.error(f"CSV parsing error in {file_path}: {e}")
        raise ValueError(f"CSV parsing error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error reading {file_path}: {e}")
        raise


def load_weather_data(file_path):
    """
    Load weather data from csv and return a list of dicts. Uses generator for efficient memory use.
    Args:
        file_path: Path to the CSV file
    Returns:
        List of dicts containing weather data
    Raises:
        FileNotFoundError: File doesn't exist
        ValueError: CSV file is empty or messed up
        Exception: Other CSV reading errors
    """
    try:
        logger.info(f"Loading weather data from: {file_path}")
        data = list(csv_row_generator(file_path))
        logger.info(f"Loaded {len(data)} records successfully")
        return data
    except Exception as e:
        logger.error(f"Failed to load weather data from {file_path}: {e}")
        raise