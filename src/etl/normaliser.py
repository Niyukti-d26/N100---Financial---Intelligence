import pandas as pd


def normalize_year(df):
    """Function: normalize_year"""
    if "year" in df.columns:
        df["year"] = df["year"].astype(str).str.extract(r"(\d{4})")[0]

        df["year"] = pd.to_numeric(df["year"], errors="coerce")

    return df


def normalize_ticker(df):
    """Function: normalize_ticker"""
    if "ticker" in df.columns:
        df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()

    return df


def normalize_text(df):
    """Function: normalize_text"""
    object_columns = df.select_dtypes(include="object").columns

    for column in object_columns:
        df[column] = df[column].astype(str).str.strip()

    return df


def normalize(df):
    """Function: normalize"""
    df = normalize_year(df)
    df = normalize_ticker(df)
    df = normalize_text(df)

    return df
