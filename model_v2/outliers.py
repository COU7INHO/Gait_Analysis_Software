import numpy as np


def remove_outliers(data):
    mean_value = np.mean(data)
    stdev_value = np.std(data)
    upper_threshold = mean_value + 3 * stdev_value
    lower_threshold = mean_value - 3 * stdev_value
    filtered_list = [x for x in data if lower_threshold <= x <= upper_threshold]
    data = filtered_list
    return data
