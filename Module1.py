import pandas as pd

def load_weather_data(file_path):
    """
    Loads weather data from csv and returns a list of dictionaries.
    """
    try:
        # load raw data
        df = pd.read_csv(file_path)

        # check if file is empty
        if df.empty:
            print("Error: the csv file is empty.")
            return []

        # convert dataframe to a list of dicts
        # I'm not very familiar with pandas so this seems like an easy way to handle right now
        weather_list = df.to_dict(orient='records')

        return weather_list

    except Exception as e:
        print(f"Error: Something went wrong.")
        return []

def print_weather_summary(weather_data):
    """
    Prints the total number of rows found in the weather data csv.
    """
    row_count = len(weather_data)
    print(f"--- Weather Data Summary ---")
    print(f"Total records found: {row_count}")

if __name__ == '__main__':
    file_name = "AustraliaWeatherData/Weather Training Data.csv"

    data = load_weather_data(file_name)
    print_weather_summary(data)