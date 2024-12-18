"""
Tests for the visualization module.
"""

import pytest
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from ..datalib.visualization import bar_plot, histogram, scatter_plot, correlation_matrix


@pytest.fixture
def data():
    """Fixture for test data."""
    return [1, 2, 3, 4, 5]


@pytest.fixture
def x_and_y_data():
    """Fixture for test data for scatter plot."""
    return [1, 2, 3, 4, 5], [5, 4, 3, 2, 1]


@pytest.fixture
def dataframe():
    """Fixture for test DataFrame."""
    return pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1],
        'C': [2, 3, 4, 5, 6]
    })


def test_bar_plot(data):
    """Test bar_plot function."""
    buf = BytesIO()
    bar_plot(data, [1, 2, 3, 4, 5])  # Using the bar_plot from visualization
    plt.savefig(buf)
    buf.seek(0)
    assert buf.getvalue() is not None


def test_histogram(data):
    """Test histogram function."""
    buf = BytesIO()
    histogram(data, bins=10)  # Using the histogram from visualization
    plt.savefig(buf)
    buf.seek(0)
    assert buf.getvalue() is not None


def test_scatter_plot(x_and_y_data):
    """Test scatter_plot function."""
    x, y = x_and_y_data
    buf = BytesIO()
    scatter_plot(x, y)  # Using the scatter_plot from visualization
    plt.savefig(buf)
    buf.seek(0)
    assert buf.getvalue() is not None


def test_correlation_matrix(dataframe):
    """Test correlation_matrix function."""
    buf = BytesIO()
    correlation_matrix(dataframe)  # Using the correlation_matrix from visualization
    plt.savefig(buf)
    buf.seek(0)
    assert buf.getvalue() is not None

