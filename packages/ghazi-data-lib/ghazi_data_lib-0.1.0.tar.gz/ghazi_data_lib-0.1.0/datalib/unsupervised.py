"""
unsupervised: Module for performing unsupervised learning tasks such as clustering and dimensionality reduction.
"""

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd


def perform_clustering(X: pd.DataFrame, n_clusters: int = 3) -> pd.Series:
    """
    Perform K-Means clustering on a dataset.

    Args:
        X (pd.DataFrame): Feature matrix for clustering.
        n_clusters (int): Number of clusters.

    Returns:
        pd.Series: Cluster labels for each data point.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X)
    return pd.Series(clusters, name="Cluster")


def apply_dimensionality_reduction(X: pd.DataFrame, n_components: int = 2) -> pd.DataFrame:
    """
    Apply Principal Component Analysis (PCA) for dimensionality reduction.

    Args:
        X (pd.DataFrame): Feature matrix for dimensionality reduction.
        n_components (int): Number of principal components.

    Returns:
        pd.DataFrame: Reduced data with principal components.
    """
    pca = PCA(n_components=n_components)
    reduced_data = pca.fit_transform(X)
    return pd.DataFrame(reduced_data, columns=[f"PC{i+1}" for i in range(n_components)])
