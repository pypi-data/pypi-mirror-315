from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier

def linear_regression(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model

def kmeans_clustering(data, n_clusters):
    model = KMeans(n_clusters=n_clusters)
    model.fit(data)
    return model

def pca_analysis(data, n_components):
    pca = PCA(n_components=n_components)
    transformed_data = pca.fit_transform(data)
    return pca, transformed_data

def decision_tree_classification(X, y):
    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model