from scipy.signal import butter, filtfilt
import numpy as np


def apply_filter(data):
    N = 10
    fc = 7
    ftype = 'lowpass'
    sample_rate = 120
    b, a = butter(N, fc / (sample_rate / 2), btype=ftype)
    filtered_data = filtfilt(b, a, data)
    return filtered_data
 
def filter_angles(data):
    if len(data) > 33:
        data = apply_filter(data)
        data = np.array(data)
    return data


    