import pandas as pd
from sklearn.datasets import load_iris
from datalib.data_processing import preprocess_dataset
from datalib.regression import  polynomial_regression
from datalib.statistics import mean, median, std_dev, correlation, t_test, chi_square
from datalib.supervised import train_supervised_model
from datalib.unsupervised import perform_clustering, apply_dimensionality_reduction
from datalib.visualization import bar_plot, histogram, scatter_plot, correlation_matrix

# 1. Load and preprocess the Iris dataset
iris_data = load_iris()
iris_df = pd.DataFrame(data=iris_data.data, columns=iris_data.feature_names)
iris_df['target'] = iris_data.target

# Preprocessing the dataset: We will drop the target column temporarily for training models
X, y = preprocess_dataset(iris_df, target_column='target', fill_missing='mean')

# 2. Descriptive Statistics
print("Mean of Sepal length:", mean(iris_df['sepal length (cm)']))
print("Median of Sepal width:", median(iris_df['sepal width (cm)']))
# print("Mode of Petal length:", mode(iris_df['petal length (cm)']))
print("Standard deviation of Petal width:", std_dev(iris_df['petal width (cm)']))

# 3. Correlation between Sepal length and Petal length
corr = correlation(iris_df['sepal length (cm)'], iris_df['petal length (cm)'])
print(f"Correlation between Sepal length and Petal length: {corr:.2f}")

# 4. Train a supervised model (Random Forest classifier) on the Iris dataset
model = train_supervised_model(X, y, model_type="classification")

# 5. Apply Clustering (KMeans)
clusters = perform_clustering(X, n_clusters=3)

# 6. Dimensionality Reduction (PCA)
reduced_data = apply_dimensionality_reduction(X, n_components=2)

# 7. Visualization
# 7.1. Correlation matrix plot
correlation_matrix(iris_df)

# 7.2. Bar plot for average of each feature
feature_means = iris_df.mean()[:-1]  # excluding target column
bar_plot(feature_means.values, feature_means.index)

# 7.3. Histogram of Sepal length
histogram(iris_df['sepal length (cm)'], bins=10)

# 7.4. Scatter plot between Sepal length and Petal length
scatter_plot(iris_df['sepal length (cm)'], iris_df['petal length (cm)'])

# 8. Perform Polynomial Regression
polynomial_model = polynomial_regression(X, y, degree=3)

# 9. Statistical Test: Chi-Square test (dummy example, using categorical data)
# For example, we'll compare the frequency of flower species
observed = iris_df['target'].value_counts().values
expected = [len(iris_df) / 3] * 3  # Assuming equal distribution of species
chi2_stat, p_val = chi_square(observed, expected)
print(f"Chi-Square test result: Statistic = {chi2_stat}, p-value = {p_val}")
