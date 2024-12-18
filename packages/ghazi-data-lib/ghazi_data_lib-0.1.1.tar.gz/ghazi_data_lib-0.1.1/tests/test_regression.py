

import pytest
import numpy as np
from sklearn.linear_model import LinearRegression
from ..datalib.regression import linear_regression, polynomial_regression

def test_linear_regression():
    """Test the linear_regression function with simple data."""
    # Prepare simple linear data: y = 2x + 1
    X = np.array([[1], [2], [3], [4], [5]])
    y = np.array([3, 5, 7, 9, 11])

    # Fit the linear regression model
    model = linear_regression(X, y)

    # Check model coefficients and intercept
    assert isinstance(model, LinearRegression)
    np.testing.assert_almost_equal(model.coef_[0], 2.0, decimal=3)
    np.testing.assert_almost_equal(model.intercept_, 1.0, decimal=3)

def test_polynomial_regression_degree_2():
    """Test the polynomial_regression function with quadratic data."""
    # Prepare quadratic data: y = x^2
    X = np.array([[1], [2], [3], [4], [5]])
    y = np.array([1, 4, 9, 16, 25])

    # Fit the polynomial regression model with degree=2
    model = polynomial_regression(X, y, degree=2)

    # Generate predictions for the input data
    from sklearn.preprocessing import PolynomialFeatures
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    predictions = model.predict(X_poly)

    # Check that predictions are close to actual y values
    np.testing.assert_almost_equal(predictions, y, decimal=3)

def test_polynomial_regression_degree_3():
    """Test the polynomial_regression function with cubic data."""
    # Prepare cubic data: y = x^3
    X = np.array([[1], [2], [3], [4], [5]])
    y = np.array([1, 8, 27, 64, 125])

    # Fit the polynomial regression model with degree=3
    model = polynomial_regression(X, y, degree=3)

    # Generate predictions for the input data
    from sklearn.preprocessing import PolynomialFeatures
    poly = PolynomialFeatures(degree=3)
    X_poly = poly.fit_transform(X)
    predictions = model.predict(X_poly)

    # Check that predictions are close to actual y values
    np.testing.assert_almost_equal(predictions, y, decimal=3)
