"""
Module de statistiques pour effectuer des analyses descriptives et des tests statistiques.

Contient des fonctions pour calculer des mesures statistiques comme la moyenne, la médiane,
le mode, l'écart-type, ainsi que des tests statistiques comme le test t et le test du chi-carré.
"""

import numpy as np
import scipy.stats as stats

def mean(data):
    """
    Calcule la moyenne des données.

    Args:
        data (list ou np.array): Une liste ou un tableau numpy contenant les valeurs numériques.

    Returns:
        float: La moyenne des données.
    """
    return np.mean(data)

def median(data):
    """
    Calcule la médiane des données.

    Args:
        data (list ou np.array): Une liste ou un tableau numpy contenant les valeurs numériques.

    Returns:
        float: La médiane des données.
    """
    return np.median(data)


def std_dev(data):
    """
    Calcule l'écart-type des données.

    Args:
        data (list ou np.array): Une liste ou un tableau numpy contenant les valeurs numériques.

    Returns:
        float: L'écart-type des données.
    """
    return np.std(data)

def correlation(data1, data2):
    """
    Calcule la corrélation entre deux ensembles de données.

    Args:
        data1 (list ou np.array): Un premier ensemble de données.
        data2 (list ou np.array): Un deuxième ensemble de données.

    Returns:
        float: Le coefficient de corrélation de Pearson entre les deux ensembles de données.
    """
    return np.corrcoef(data1, data2)[0, 1]

def t_test(data1, data2):
    """
    Effectue un test t de Student pour comparer deux ensembles de données.

    Args:
        data1 (list ou np.array): Le premier ensemble de données.
        data2 (list ou np.array): Le deuxième ensemble de données.

    Returns:
        tuple: Un tuple contenant la statistique t et la valeur p du test t.
    """
    return stats.ttest_ind(data1, data2)

def chi_square(observed, expected):
    """
    Effectue un test du chi-carré pour comparer les distributions observée et attendue.

    Args:
        observed (list ou np.array): La distribution observée.
        expected (list ou np.array): La distribution attendue.

    Returns:
        tuple: Un tuple contenant la statistique du chi-carré et la valeur p du test.
    """
    return stats.chisquare(observed, expected)
