import math

# originally did this in main() but got messy so decided it needed its own function
def extract_valid_temperatures(data, column_name):
    """
    Extracts valid temp values from weather data. Filters out None and NaN values.
    Args:
        data: List of dicts containing weather data
        column_name: Name of the temp column to extract
    Returns:
        List of valid temp values (floats)
    Raises:
        ValueError: If data is empty or column_name doesn't exist in data
    """
    if not data:
        raise ValueError("Can't extract temperatures from empty dataset")

    # verify column exists in first row
    if column_name not in data[0]:
        raise ValueError(f"Column '{column_name}' not found in dataset")

    valid_temps = []
    for row in data:
        val = row.get(column_name)
        if val is not None and not math.isnan(val):
            valid_temps.append(val)

    return valid_temps
