from src.screener.engine import ScreenerEngine


def test_value_pick():

    engine = ScreenerEngine()

    df = engine.value_pick()

    assert len(df) > 0

    assert (df["pe_ratio"] <= 20).all()
    assert (df["pb_ratio"] <= 3).all()
    assert (df["dividend_yield_pct"] >= 1).all()

    non_financial = df[df["broad_sector"] != "Financials"]

    assert (non_financial["debt_to_equity"] <= 2).all()