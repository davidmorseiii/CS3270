import weather_analysis as wa

def main():
    file_name = "AustraliaWeatherData/Weather Test Data.csv"
    print("-- Weather Analysis --")

    try:
        # 1. Create the WeatherDataset object to handle loading its own data
        dataset = wa.WeatherDataset(file_name)
        print(f"Total rows: {dataset.get_row_count()}")

        # 2. Analyze MaxTemp
        # ask the object for the stats rather than calculating manually here
        max_stats = dataset.get_column_statistics('MaxTemp')
        
        if max_stats:
            print("\n-- MaxTemp Statistics --")
            print(f"Mean:   {max_stats['mean']:.2f}")
            print(f"Median: {max_stats['median']:.2f}")
            print(f"Range:  {max_stats['range']:.2f}")
        else:
            print("Error: no valid MaxTemp data found.")

        # 3. Analyze MinTemp
        min_stats = dataset.get_column_statistics('MinTemp')
        
        if min_stats:
            print("\n-- MinTemp Statistics --")
            print(f"Mean:   {min_stats['mean']:.2f}")
            print(f"Median: {min_stats['median']:.2f}")
            print(f"Range:  {min_stats['range']:.2f}")
        else:
            print("Error: no valid MinTemp data found.")

    except FileNotFoundError:
        print(f"Error: file '{file_name}' not found.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == '__main__':
    main()