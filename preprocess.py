import pandas as pd


FILE_PATH = "./WID_DATA_02062021-090326.csv"


def load():

    df = pd.read_csv(
        FILE_PATH,
        engine='c',
        sep=';',
        skiprows=1,
        header=None,
        usecols=[0, 3, 4],
        names=["country", "year", "value"]
        )

    return df


def clean(df):

    def convert_to_float(var):
        try:
            return float(var)
        except(ValueError):
            return -1 

    df = df.copy(deep=True)

    df.loc[df.value.isna(), "value"] = -1
    df["value"] = df.value.apply(convert_to_float)

    return df




if __name__ == "__main__":

    df = load()
    df = clean(df)
    df.to_csv("WID_clean.csv", index=False)


