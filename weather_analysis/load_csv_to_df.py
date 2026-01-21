import pandas as pd
import os

def load_weather_data(file_path):
    """
    Loads weather data from csv and returns a list of dictionaries.

    Args:
        file_path: Path to the CSV file

    Returns:
        List of dictionaries containing weather data

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the CSV file is empty
        Exception: For other pandas/CSV reading errors
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # load raw data
    df = pd.read_csv(file_path)

    # check if file is empty
    if df.empty:
        raise ValueError("The CSV file is empty")

    # convert dataframe to a list of dicts
    # I'm not very familiar with pandas so this seems like an easy way to handle right now
    return df.to_dict(orient='records')