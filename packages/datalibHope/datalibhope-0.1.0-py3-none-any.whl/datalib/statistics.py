import numpy as np

def calculate_mean(data):
    return np.mean(data)

def calculate_median(data):
    return np.median(data)

def calculate_mode(data):
    return data.mode()[0]

def calculate_standard_deviation(data):
    return np.std(data)

def correlation_coefficient(data1, data2):
    return np.corrcoef(data1, data2)[0, 1]
