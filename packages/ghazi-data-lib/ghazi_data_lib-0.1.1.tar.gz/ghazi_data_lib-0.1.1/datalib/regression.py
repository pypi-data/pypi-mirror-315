"""
Module de régression pour effectuer des régressions linéaire et polynomiale.

Ce module fournit des fonctions pour ajuster des modèles de régression linéaire et
polynomiale sur des données d'entrée, en vue de prédictions basées sur ces modèles.
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def linear_regression(X, y):
    """
    Effectue une régression linéaire sur les données d'entrée.

    Args:
        X (array-like): Les variables indépendantes (features).
        y (array-like): La variable dépendante (target).

    Returns:
        model (LinearRegression): Le modèle de régression linéaire ajusté.
    """
    model = LinearRegression()
    model.fit(X, y)
    return model

def polynomial_regression(X, y, degree=2):
    """
    Effectue une régression polynomiale sur les données d'entrée.

    Args:
        X (array-like): Les variables indépendantes (features).
        y (array-like): La variable dépendante (target).
        degree (int, optionnel): Le degré du polynôme (par défaut 2).

    Returns:
        model (LinearRegression): Le modèle de régression polynomiale ajusté.
    """
    poly = PolynomialFeatures(degree)
    X_poly = poly.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, y)
    return model
