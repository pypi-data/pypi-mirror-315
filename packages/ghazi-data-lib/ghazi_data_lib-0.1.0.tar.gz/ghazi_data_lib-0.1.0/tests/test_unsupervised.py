"""
Tests for the unsupervised module.
"""

import pytest
import pandas as pd
from ..datalib.unsupervised import perform_clustering, apply_dimensionality_reduction

def test_perform_clustering():
    """Test K-Means clustering function."""
    # Generate synthetic data for clustering
    data = pd.DataFrame({
        "feature1": [1, 2, 3, 8, 9, 10],
        "feature2": [1, 2, 3, 8, 9, 10],
    })

    # Perform clustering
    clusters = perform_clustering(data, n_clusters=2)

    # Validate the output
    assert len(clusters) == len(data), "Cluster output length mismatch."
    assert clusters.nunique() == 2, "Number of clusters should be 2."
    assert clusters.name == "Cluster", "Cluster column name should be 'Cluster'."

def test_apply_dimensionality_reduction():
    """Test PCA dimensionality reduction function."""
    # Generate synthetic data
    data = pd.DataFrame({
        "feature1": [1, 2, 3, 4, 5],
        "feature2": [2, 3, 4, 5, 6],
        "feature3": [5, 6, 7, 8, 9],
    })

    # Apply PCA for 2 components
    reduced_data = apply_dimensionality_reduction(data, n_components=2)

    # Validate the output
    assert reduced_data.shape == (5, 2), "Reduced data shape mismatch."
    assert list(reduced_data.columns) == ["PC1", "PC2"], "PCA column names mismatch."

def test_clustering_invalid_n_clusters():
    """Test clustering with invalid n_clusters."""
    data = pd.DataFrame({
        "feature1": [1, 2, 3],
        "feature2": [4, 5, 6],
    })
    with pytest.raises(ValueError, match="n_clusters"):
        perform_clustering(data, n_clusters=0)


