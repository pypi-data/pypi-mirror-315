"""
Tests for the data_processing module.
"""

import pytest
import pandas as pd
from io import StringIO
from ..datalib.data_processing import load_dataset, preprocess_dataset


# Mocked CSV data for testing load_dataset
CSV_DATA = """
id,name,age,salary,target
1,Alice,30,50000,1
2,Bob,,60000,0
3,Charlie,25,,1
4,David,40,70000,0
"""

@pytest.fixture
def mock_csv_file(tmp_path):
    """Fixture to create a temporary CSV file."""
    file = tmp_path / "test.csv"
    file.write_text(CSV_DATA)
    return str(file)


def test_load_dataset(mock_csv_file):
    """Test loading a dataset from a CSV file."""
    df = load_dataset(mock_csv_file)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["id", "name", "age", "salary", "target"]
    assert df.shape == (4, 5)  # 4 rows, 5 columns


def test_preprocess_dataset_drop_columns():
    """Test preprocessing with dropping specific columns."""
    data = pd.DataFrame({
        "id": [1, 2, 3],
        "feature1": [10, 20, 30],
        "feature2": [40, 50, 60],
        "target": [0, 1, 0],
    })
    X, y = preprocess_dataset(data, target_column="target", drop_columns=["id"])
    assert "id" not in X.columns
    assert "target" not in X.columns
    assert list(y) == [0, 1, 0]
    assert X.shape == (3, 2)


def test_preprocess_dataset_fill_missing_mean():
    """Test preprocessing with missing value handling (mean)."""
    data = pd.DataFrame({
        "feature1": [10, None, 30],
        "feature2": [40, 50, None],
        "target": [0, 1, 0],
    })
    X, y = preprocess_dataset(data, target_column="target", fill_missing="mean")
    assert X.isnull().sum().sum() == 0  # No missing values
    assert round(X["feature1"].iloc[1]) == 20  # Mean of 10 and 30
    assert round(X["feature2"].iloc[2]) == 45  # Mean of 40 and 50


def test_preprocess_dataset_fill_missing_median():
    """Test preprocessing with missing value handling (median)."""
    data = pd.DataFrame({
        "feature1": [10, None, 30],
        "feature2": [40, 50, None],
        "target": [0, 1, 0],
    })
    X, y = preprocess_dataset(data, target_column="target", fill_missing="median")
    assert X.isnull().sum().sum() == 0  # No missing values
    assert X["feature1"].iloc[1] == 20  # Median of 10 and 30
    assert X["feature2"].iloc[2] == 45  # Median of 40 and 50


def test_preprocess_dataset_no_target():
    """Test preprocessing without specifying a target column."""
    data = pd.DataFrame({
        "feature1": [1, 2, 3],
        "feature2": [4, 5, 6],
    })
    X, y = preprocess_dataset(data)
    assert y is None
    assert X.shape == (3, 2)
    assert list(X.columns) == ["feature1", "feature2"]

