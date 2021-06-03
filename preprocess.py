import pandas as pd


FILE_PATH = "./WID_DATA_02062021-120038.csv"


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


def clean_value_field(df):

    def convert_to_float(var):
        try:
            return float(var)
        except(ValueError):
            return -1 

    df = df.copy(deep=True)

    df.loc[df.value.isna(), "value"] = -1
    df["value"] = df.value.apply(convert_to_float)

    df = df.loc[df.value > 0]

    df["value"] *= 100

    return df


def add_country_code(df):

    df = df.copy(deep=True)

    country_nms_to_drop = ['Macao', 'Myanmar', 'Palestine', 'Zanzibar']
    df = df.loc[~df.country.isin(country_nms_to_drop)]
    df.country.replace({
        "Korea":"Korea, South",
        "North Korea":"Korea, North",
        "Viet Nam":"Vietnam",
        "USA":"United States",
        "Brunei Darussalam":"Brunei",
        "Cote d’Ivoire":"Cote d'Ivoire",
        "Lao PDR":"Laos",
        "Syrian Arab Republic":"Syria",
        "Russian Federation":"Russia"
        }, inplace=True)


    country_nm_to_code_df = pd.read_csv(
        'https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv',
        usecols=["COUNTRY", "CODE"]
        )
    country_nm_to_code_df.columns = [col_nm.lower() for col_nm in country_nm_to_code_df.columns]
    country_nm_to_code_df.country.replace({
        "Bahamas, The":"Bahamas",
        "Congo, Republic of the":"Congo",
        "Congo, Democratic Republic of the": "DR Congo",
        "Gambia, The": "Gambia",

    }, inplace=True)

    df = df.merge(country_nm_to_code_df, on="country", how="left")

    return df



if __name__ == "__main__":

    df = load()
    df = clean_value_field(df)
    df = add_country_code(df)
    df.to_csv("WID_clean.csv", index=False)


