def recommend_chart(data_analysis):
    if len(data_analysis['columns']) == 1:
        return "Histogram"
    elif len(data_analysis['columns']) == 2:
        return "Scatter Plot"
    else:
        return "Heatmap"
