import pandas as pd


def read_excel(path):

    df = pd.read_excel(path)

    required_columns = {
        "przewinienie",
        "kara"
    }

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "Plik Excel musi zawierać kolumny: przewinienie, kara"
        )


    result = []

    for _, row in df.iterrows():

        result.append(
            {
                "przewinienie": str(row["przewinienie"]),
                "kara": str(row["kara"])
            }
        )


    return result