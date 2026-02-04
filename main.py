import sys
from weather_analysis import WeatherDataset
from weather_analysis.logger_config import setup_logger

logger = setup_logger('main')

def main():
    """Run weather analysis"""
    file_name = "AustraliaWeatherData/Weather Test Data.csv"

    try:
        logger.info("Starting weather analysis application")

        # Create the WeatherDataset object to handle loading its own data
        logger.info(f"Loading dataset from: {file_name}")
        dataset = WeatherDataset(file_name)

        print("-- Weather Analysis --")
        row_count = dataset.get_row_count()
        print(f"Total rows: {row_count}")
        logger.info(f"Dataset contains {row_count} rows")

        # MaxTemp
        logger.info("Analyzing MaxTemp column")
        max_stats = dataset.get_column_statistics('MaxTemp')

        print("-- MaxTemp Statistics --")
        print(f"Mean:   {max_stats['mean']:.2f}")
        print(f"Median: {max_stats['median']:.2f}")
        print(f"Range:  {max_stats['range']:.2f}")
        logger.info(f"MaxTemp analysis complete: mean={max_stats['mean']:.2f}")

        # MinTemp
        logger.info("Analyzing MinTemp column")
        min_stats = dataset.get_column_statistics('MinTemp')

        print("-- MinTemp Statistics --")
        print(f"Mean:   {min_stats['mean']:.2f}")
        print(f"Median: {min_stats['median']:.2f}")
        print(f"Range:  {min_stats['range']:.2f}")
        logger.info(f"MinTemp analysis complete: mean={min_stats['mean']:.2f}")

        logger.info("Weather analysis completed successfully")

    except FileNotFoundError as e:
        logger.error(f"File not found: {file_name}", exc_info=True)
        print(f"Error: file '{file_name}' not found.")
        sys.exit(1)

    except ValueError as e:
        logger.error(f"Value error: {e}", exc_info=True)
        print(f"Error: {e}")
        sys.exit(1)

    except PermissionError as e:
        logger.error(f"Permission error accessing file: {file_name}", exc_info=True)
        print(f"Error: permission denied when accessing '{file_name}'.")
        sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
        print("\nAnalysis interrupted by user.")
        sys.exit(0)

    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()