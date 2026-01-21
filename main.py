import weather_analysis as wa

def main():
    file_name = "AustraliaWeatherData/Weather Test Data.csv"
    print("-- Weather Analysis --")

    try:
        #1. Load data
        data = wa.load_weather_data(file_name)
        print(f"Total rows: {len(data)}")

        #2. Extract and clean data
        max_temps = wa.extract_valid_temperatures(data, 'MaxTemp')
        min_temps = wa.extract_valid_temperatures(data, 'MinTemp')

        #3. Calculate and display stats for MaxTemp
        if max_temps:
            print("\n-- MaxTemp Statistics --")
            print(f'Mean:   {wa.calculate_mean(max_temps):.2f}')
            print(f'Median: {wa.calculate_median(max_temps):.2f}')
            print(f'Range:  {wa.calculate_range(max_temps):.2f}')
        else:
            print("Error: no valid MaxTemp data found.")

        #4. Calculate and display stats for MinTemp
        if min_temps:
            print("\n-- MinTemp Statistics --")
            print(f'Mean:   {wa.calculate_mean(min_temps):.2f}')
            print(f'Median: {wa.calculate_median(min_temps):.2f}')
            print(f'Range:  {wa.calculate_range(min_temps):.2f}')
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