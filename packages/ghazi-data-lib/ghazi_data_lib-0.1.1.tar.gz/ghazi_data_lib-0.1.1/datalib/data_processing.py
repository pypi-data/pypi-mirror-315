"""
data_processing: Module for loading, cleaning, and preprocessing datasets.
"""

import pandas as pd
from typing import Tuple, Optional, List


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load a dataset from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset as a DataFrame.
    """
    return pd.read_csv(file_path)


def preprocess_dataset(
    df: pd.DataFrame,
    target_column: Optional[str] = None,
    drop_columns: Optional[List[str]] = None,
    fill_missing: str = "mean",
) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
    """
    Preprocess the dataset for machine learning tasks.

    Args:
        df (pd.DataFrame): Input dataset.
        target_column (Optional[str]): Name of the target column for supervised learning.
        drop_columns (Optional[List[str]]): Columns to drop from the dataset.
        fill_missing (str): Strategy to fill missing values ("mean" or "median").

    Returns:
        Tuple[pd.DataFrame, Optional[pd.Series]]:
            - X (pd.DataFrame): Features (input variables).
            - y (Optional[pd.Series]): Target variable, if specified.
    """
    if drop_columns:
        df = df.drop(columns=drop_columns)

    if fill_missing == "mean":
        df = df.fillna(df.mean())
    elif fill_missing == "median":
        df = df.fillna(df.median())

    if target_column:
        X = df.drop(columns=[target_column])
        y = df[target_column]
        return X, y

    return df, None
