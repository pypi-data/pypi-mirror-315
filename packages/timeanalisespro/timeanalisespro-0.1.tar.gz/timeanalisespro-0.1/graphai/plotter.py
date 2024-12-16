import matplotlib.pyplot as plt

def generate_chart(data, chart_type):
    if chart_type == "Histogram":
        data.hist()
    elif chart_type == "Scatter Plot":
        plt.scatter(data.iloc[:, 0], data.iloc[:, 1])
    elif chart_type == "Heatmap":
        import seaborn as sns
        sns.heatmap(data.corr(), annot=True, fmt=".2f")
    plt.show()
