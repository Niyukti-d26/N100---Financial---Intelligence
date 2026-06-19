import pandas as pd
import pytest

from src.etl.normaliser import normalize_year, normalize_ticker


@pytest.mark.parametrize(
    "value,expected",
    [
        ("2023", 2023),
        ("FY2022", 2022),
        ("2021-22", 2021),
        ("2019", 2019),
        (2020, 2020),
        (2021.0, 2021),
        ("FY2018-19", 2018),
        ("Year2024", 2024),
        (" 2025 ", 2025),
        ("2026 Annual", 2026),
        ("abcd", None),
        ("", None),
        (None, None),
        ("----", None),
        ("FY", None),
        ("20", None),
        ("abc2023xyz", 2023),
        ("2027/28", 2027),
        ("FY 2028", 2028),
        ("2029*", 2029),
    ],
)
def test_normalize_year(value, expected):

    df = pd.DataFrame({"year": [value]})

    result = normalize_year(df)

    if expected is None:
        assert pd.isna(result["year"][0])
    else:
        assert result["year"][0] == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("tcs", "TCS"),
        (" infy ", "INFY"),
        ("hdfc", "HDFC"),
        (" axis ", "AXIS"),
        ("RELIANCE", "RELIANCE"),
        ("m&m", "M&M"),
        ("lt", "LT"),
        ("123", "123"),
        (123, "123"),
        ("", ""),
        (None, None),
        (" adani ", "ADANI"),
        ("itc", "ITC"),
        ("SBIN", "SBIN"),
        ("tatamotors", "TATAMOTORS"),
    ],
)
def test_normalize_ticker(value, expected):

    df = pd.DataFrame({"ticker": [value]})

    result = normalize_ticker(df)

    if expected is None:
        assert pd.isna(result["ticker"][0])
    else:
        assert result["ticker"][0] == expected


def test_year_column_missing():

    df = pd.DataFrame({"sales": [100]})

    result = normalize_year(df)

    assert "sales" in result.columns


def test_ticker_column_missing():

    df = pd.DataFrame({"sales": [100]})

    result = normalize_ticker(df)

    assert "sales" in result.columns