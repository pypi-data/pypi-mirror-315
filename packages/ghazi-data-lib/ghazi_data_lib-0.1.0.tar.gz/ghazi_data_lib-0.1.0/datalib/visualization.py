"""
Module de visualisation de données pour générer différents types de graphiques.

Ce module contient des fonctions pour créer des graphiques simples comme des diagrammes
en barres, des histogrammes et des nuages de points, ainsi que des visualisations avancées
comme les matrices de corrélation.
"""


import matplotlib.pyplot as plt
import seaborn as sns


def bar_plot(data, labels):
    """
    Génère un graphique en barres.

    Args:
        data (list ou np.array): Les valeurs à afficher.
        labels (list): Les étiquettes des barres.

    Returns:
        None
    """
    plt.bar(labels, data)
    plt.xlabel("Labels")
    plt.ylabel("Values")
    plt.title("Bar Plot")
    plt.show()

def histogram(data, bins=10):
    """
    Génère un histogramme des données.

    Args:
        data (list ou np.array): Les données à afficher.
        bins (int, optionnel): Le nombre de bins (par défaut 10).

    Returns:
        None
    """
    plt.hist(data, bins=bins, edgecolor='black')
    plt.xlabel("Values")
    plt.ylabel("Frequency")
    plt.title("Histogram")
    plt.show()

def scatter_plot(x, y):
    """
    Génère un nuage de points.

    Args:
        x (list ou np.array): Les valeurs sur l'axe des X.
        y (list ou np.array): Les valeurs sur l'axe des Y.

    Returns:
        None
    """
    plt.scatter(x, y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Scatter Plot")
    plt.show()

def correlation_matrix(data):
    """
    Affiche une matrice de corrélation sous forme de carte thermique.

    Args:
        data (DataFrame ou np.array): Un tableau contenant les données numériques.

    Returns:
        None
    """
    corr = data.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.show()
