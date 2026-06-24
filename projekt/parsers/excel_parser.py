import pandas as pd


def read_excel(path):

    df = pd.read_excel(path)

    result = []

    for _, row in df.iterrows():

        result.append(
            {
                "przewinienie": row["przewinienie"],
                "kara": row["kara"]
            }
        )

    return result