import matplotlib.pyplot as plt
import seaborn as sns

def plot_bar(data, title="Bar Chart", xlabel="X-axis", ylabel="Y-axis"):
    data.plot(kind='bar')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def plot_histogram(data, bins=10, title="Histogram", xlabel="X-axis", ylabel="Y-axis"):
    data.plot(kind='hist', bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def plot_scatter(x, y, title="Scatter Plot", xlabel="X-axis", ylabel="Y-axis"):
    plt.scatter(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def plot_correlation_matrix(data):
    correlation = data.corr()
    sns.heatmap(correlation, annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.show()