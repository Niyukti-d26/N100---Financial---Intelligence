from src.screener.engine import ScreenerEngine


def test_growth_accelerator():

    engine = ScreenerEngine()

    df = engine.growth_accelerator()

    assert len(df) > 0

    assert (df["pat_cagr_5yr"] >= 20).all()
    assert (df["revenue_cagr_5yr"] >= 15).all()

    non_financial = df[df["broad_sector"] != "Financials"]

    assert (non_financial["debt_to_equity"] <= 2).all()