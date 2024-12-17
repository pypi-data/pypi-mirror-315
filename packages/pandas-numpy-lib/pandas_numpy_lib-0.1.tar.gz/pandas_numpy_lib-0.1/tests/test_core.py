# tests/test_core.py

import pytest
import numpy as np
import pandas as pd
from pandas_numpy_lib import create_dataframe_from_array, add_column_to_dataframe, normalize_column

def test_create_dataframe_from_array():
    arr = np.array([[1, 2], [3, 4], [5, 6]])
    df = create_dataframe_from_array(arr)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (3, 2)

def test_add_column_to_dataframe():
    arr = np.array([[1, 2], [3, 4], [5, 6]])
    df = create_dataframe_from_array(arr)
    new_col = np.array([7, 8, 9])
    df = add_column_to_dataframe(df, "new_col", new_col)
    assert "new_col" in df.columns
    assert df["new_col"].equals(pd.Series([7, 8, 9]))

def test_normalize_column():
    arr = np.array([[1, 2], [3, 4], [5, 6]])
    df = create_dataframe_from_array(arr)
    df = normalize_column(df, "0")
    assert df["0"].max() == 1
    assert df["0"].min() == 0
