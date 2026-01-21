import pandas as pd
import os

def load_weather_data(file_path):
    """
    Loads weather data from csv and returns a list of dictionaries.
    """
    if not os.path.exists(file_path):
        print(f"Error: file not found.")
        return []

    try:
        # load raw data
        df = pd.read_csv(file_path)
        # check if file is empty
        if df.empty:
            print("Error: the csv file is empty.")
            return []

        # convert dataframe to a list of dicts
        # I'm not very familiar with pandas so this seems like an easy way to handle right now
        return df.to_dict(orient='records')

    except Exception as e:
        print(f"Error reading file: {e}")
        return []

if __name__ == '__main__':
    file_name = "AustraliaWeatherData/Weather Training Data.csv"

    data = load_weather_data(file_name)