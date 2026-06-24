import pandas as pd


def read_excel(path):

    df = pd.read_excel(path)

    return df.to_string()