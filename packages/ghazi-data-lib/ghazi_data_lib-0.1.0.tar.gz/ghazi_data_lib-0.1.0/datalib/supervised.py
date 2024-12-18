"""
supervised: Module for training supervised machine learning models.
"""

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor


def train_supervised_model(
    X,
    y,
    model_type: str = "classification",
    test_size: float = 0.2,
    random_state: int = 42,
):
    """
    Train a supervised learning model (classification or regression).

    Args:
        X (pd.DataFrame or array-like): Feature matrix.
        y (pd.Series or array-like): Target vector.
        model_type (str): Type of model ("classification" or "regression").
        test_size (float): Proportion of the data for the test set.
        random_state (int): Random seed for reproducibility.

    Returns:
        model: Trained machine learning model.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    if model_type == "classification":
        model = RandomForestClassifier(random_state=random_state)
    elif model_type == "regression":
        model = RandomForestRegressor(random_state=random_state)
    else:
        raise ValueError("Invalid model_type. Choose 'classification' or 'regression'.")

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    if model_type == "classification":
        score = accuracy_score(y_test, predictions)
        print(f"Accuracy: {score:.2f}")
    elif model_type == "regression":
        score = mean_squared_error(y_test, predictions, squared=False)
        print(f"RMSE: {score:.2f}")

    return model
