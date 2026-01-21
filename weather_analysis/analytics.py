import statistics

def calculate_mean(values):
    """
    Calcs the average of list of numbers
    Args:
        values: List of number values
    Returns:
        Mean value (float) or 0 if list is empty
    """
    if not values:
        return 0

    # sum divided by count
    total = sum(values)
    count = len(values)
    return total / count

def calculate_median(values):
    """
    Calcs the median of list of numbers.
    Args:
        values: List of number values
    Returns:
        Median value (float), or 0 if list is empty
    """
    if not values:
        return 0

    sorted_values = sorted(values)
    n = len(sorted_values)

    # if odd number of elements, return middle value
    if n % 2 == 1:
        return sorted_values[n // 2]
    # if even number of elements, return avg of two middle values
    else:
        mid1 = sorted_values[n // 2 - 1]
        mid2 = sorted_values[n // 2]
        return (mid1 + mid2) / 2

def calculate_range(values):
    """
    Calculates the range (max - min) of list of numbers.
    Args:
        values: List of number values
    Returns:
        Range value (float), or 0 if list is empty
    """
    if not values:
        return 0

    return max(values) - min(values)