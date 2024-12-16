import pandas as pd

def analyze_data(data):
    analysis = {
        "columns": data.columns.tolist(),
        "types": data.dtypes.apply(lambda x: x.name).to_dict(),
        "summary": data.describe(include='all').to_dict(),
    }
    return analysis
