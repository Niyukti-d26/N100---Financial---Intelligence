from src.screener.engine import ScreenerEngine


def test_quality_compounder():

    engine = ScreenerEngine()

    df = engine.quality_compounder()

    assert len(df) > 0

    assert (
        df["return_on_equity_pct"] >= 15
    ).all()

    non_financial = df[
        df["broad_sector"] != "Financials"
    ]

    assert (
        non_financial["debt_to_equity"] <= 1
    ).all()

    assert (
        df["free_cash_flow_cr"] >= 0
    ).all()

    assert (
        df["revenue_cagr_5yr"] >= 10
    ).all()