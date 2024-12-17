# pandas_numpy_lib/core.py

import pandas as pd
import numpy as np

def create_dataframe_from_array(arr):
    """
    Converts a numpy array into a pandas DataFrame.
    """
    return pd.DataFrame(arr)

def add_column_to_dataframe(df, column_name, values):
    """
    Adds a column to an existing pandas DataFrame from a numpy array.
    """
    df[column_name] = values
    return df

def normalize_column(df, column_name):
    """
    Normalizes a column in the DataFrame using numpy.
    """
    df[column_name] = (df[column_name] - np.min(df[column_name])) / (np.max(df[column_name]) - np.min(df[column_name]))
    return df
