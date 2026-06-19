import pandas as pd


def normalize_year(df):
    if "year" in df.columns:
        df["year"] = (
            df["year"]
            .astype(str)
            .str.extract(r"(\d{4})")[0]
        )

        df["year"] = pd.to_numeric(df["year"], errors="coerce")

    return df


def normalize_ticker(df):
    if "ticker" in df.columns:
        df["ticker"] = (
            df["ticker"]
            .astype(str)
            .str.upper()
            .str.strip()
        )

    return df


def normalize_text(df):
    object_columns = df.select_dtypes(include="object").columns

    for column in object_columns:
        df[column] = df[column].astype(str).str.strip()

    return df


def normalize(df):
    df = normalize_year(df)
    df = normalize_ticker(df)
    df = normalize_text(df)

    return df