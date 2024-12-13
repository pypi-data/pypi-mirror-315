import pandas as pd
import numpy as np

def load_csv(filepath):
    return pd.read_csv(filepath)

def save_csv(data, filepath):
    data.to_csv(filepath, index=False)

def normalize_data(data):
    return (data - data.min()) / (data.max() - data.min())

def handle_missing_values(data, method="mean"):
    if method == "mean":
        return data.fillna(data.mean())
    elif method == "median":
        return data.fillna(data.median())
    elif method == "drop":
        return data.dropna()
    else:
        raise ValueError("Invalid method. Use 'mean', 'median', or 'drop'.")