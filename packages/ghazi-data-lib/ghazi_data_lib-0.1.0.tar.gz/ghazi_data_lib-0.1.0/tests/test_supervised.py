"""
Tests for the supervised module.
"""

import pytest
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, mean_squared_error
from ..datalib.supervised import train_supervised_model

def test_train_classification_model(capfd):
    """Test training a classification model."""
    # Generate sample classification data
    X = pd.DataFrame({
        "feature1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "feature2": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    })
    y = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]  # Binary target variable

    # Train the classification model
    model = train_supervised_model(X, y, model_type="classification")

    # Check if the model is an instance of RandomForestClassifier
    from sklearn.ensemble import RandomForestClassifier
    assert isinstance(model, RandomForestClassifier)

    # Capture the printed accuracy and validate the output
    captured = capfd.readouterr()
    assert "Accuracy" in captured.out

    
def test_invalid_model_type():
    """Test that an invalid model type raises a ValueError."""
    X = np.array([[1, 2], [3, 4]])
    y = [0, 1]

    with pytest.raises(ValueError, match="Invalid model_type"):
        train_supervised_model(X, y, model_type="invalid")
