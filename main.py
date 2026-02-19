import sys
from weather_analysis import (
    WeatherDataset,
    filter_by_rainfall_threshold,
    filter_high_temperature_days,
    filter_windy_days,
    calculate_total_rainfall,
    find_max_temperature,
    find_min_temperature,
    count_rainy_days,
    analyze_rain_patterns,
    extract_temperature_range,
    plot_temperature_distribution,
    plot_rainfall_patterns,
    plot_temperature_vs_humidity,
    plot_wind_speed_distribution,
    plot_pressure_vs_rain,
    plot_temperature_range_trends
)
from weather_analysis.logger_config import setup_logger

logger = setup_logger('main')

def main():
    """Run weather analysis with data visualization"""
    file_name = "AustraliaWeatherData/Weather Training Data.csv"

    try:
        logger.info("Starting weather analysis application")

        # Create WeatherDataset object to handle loading its own data
        logger.info(f"Loading dataset from: {file_name}")
        dataset = WeatherDataset(file_name)

        print("=" * 60)
        print("WEATHER DATA ANALYSIS - Module 6")
        print("Data Patterns, Trends, and Visualization")
        print("=" * 60)

        row_count = dataset.get_row_count()
        print(f"\nTotal rows in dataset: {row_count:,}")
        logger.info(f"Dataset contains {row_count} rows")

        # Get the data for analysis
        data = dataset.get_data()

        # Pattern Analysis
        print("\n" + "=" * 60)
        print("PATTERN ANALYSIS (using map, filter, lambda, reduce)")
        print("=" * 60)

        # Rain patterns
        print("\n-- Rain Pattern Analysis --")
        rain_patterns = analyze_rain_patterns(data)
        print(f"Days with rain today:     {rain_patterns['rain_today']:,}")
        print(f"Days with rain tomorrow:  {rain_patterns['rain_tomorrow']:,}")
        print(f"Consecutive rainy days:   {rain_patterns['consecutive_rain']:,}")
        print(f"Rain today percentage:    {rain_patterns['rain_today']/rain_patterns['total_days']*100:.1f}%")

        # Temp extremes using reduce
        print("\n-- Temperature Extremes (using reduce) --")
        max_temp = find_max_temperature(data)
        min_temp = find_min_temperature(data)
        print(f"Highest recorded temp:    {max_temp:.1f}°C")
        print(f"Lowest recorded temp:     {min_temp:.1f}°C")
        print(f"Overall range:            {max_temp - min_temp:.1f}°C")

        # Total rainfall using reduce
        print("\n-- Total Rainfall (using reduce) --")
        total_rainfall = calculate_total_rainfall(data)
        print(f"Total rainfall:           {total_rainfall:,.1f} mm")
        print(f"Average per day:          {total_rainfall/row_count:.2f} mm")

        # Filter high temp days with filter and lambda
        print("\n-- High Temperature Days (using filter/lambda) --")
        hot_days = filter_high_temperature_days(data, 35.0)
        print(f"Days with MaxTemp >= 35°C: {len(hot_days):,}")
        print(f"Percentage of dataset:     {len(hot_days)/row_count*100:.2f}%")

        # Filter heavy rainfall days with filter and lambda
        print("\n-- Heavy Rainfall Days (using filter/lambda) --")
        heavy_rain_days = filter_by_rainfall_threshold(data, 10.0)
        print(f"Days with Rainfall >= 10mm: {len(heavy_rain_days):,}")
        print(f"Percentage of dataset:      {len(heavy_rain_days)/row_count*100:.2f}%")

        # Filter windy days with filter and lambda
        print("\n-- Windy Days (using filter/lambda) --")
        windy_days = filter_windy_days(data, 60.0)
        print(f"Days with WindGust >= 60 km/h: {len(windy_days):,}")
        print(f"Percentage of dataset:         {len(windy_days)/row_count*100:.2f}%")

        # Tempe range analysis with map and lambda
        print("\n-- Daily Temperature Range (using map/lambda) --")
        temp_ranges = extract_temperature_range(data)
        if temp_ranges:
            avg_range = sum(temp_ranges) / len(temp_ranges)
            max_range = max(temp_ranges)
            min_range = min(temp_ranges)
            print(f"Average daily range:  {avg_range:.2f}°C")
            print(f"Largest daily range:  {max_range:.2f}°C")
            print(f"Smallest daily range: {min_range:.2f}°C")

        # Data Visualization
        print("\n" + "=" * 60)
        print("GENERATING VISUALIZATIONS")
        print("=" * 60)

        print("\nCreating charts...")

        # Generate visualizations
        plot_temperature_distribution(data, 'temperature_distribution.png')
        print("✓ Temperature distirbution histogram saved")

        plot_rainfall_patterns(data, 'rainfall_patterns.png')
        print("✓ Rainfall patterns histogram saved")

        plot_temperature_vs_humidity(data, 'temp_vs_humidity.png')
        print("✓ Temperature vs Humidity scatter plot saved")

        plot_wind_speed_distribution(data, 'wind_speed_distribution.png')
        print("✓ Wind speed distribution histogram saved")

        plot_pressure_vs_rain(data, 'pressure_vs_rain.png')
        print("✓ Pressure vs Rain comparison box plot saved")

        plot_temperature_range_trends(data, 'temperature_range_trends.png')
        print("✓ Temperature range trends histogram saved")

        print("\n" + "=" * 60)
        print("ANAYLSIS COMPLETE")
        print("=" * 60)
        print("\nAll visualizations saved to current directory.")

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