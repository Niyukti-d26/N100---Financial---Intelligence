from src.screener.engine import ScreenerEngine


def test_turnaround_watch():

    engine = ScreenerEngine()

    df = engine.turnaround_watch()

    assert len(df) > 0

    assert (df["free_cash_flow_cr"] >= 0).all()
    assert (df["revenue_cagr_5yr"] >= 10).all()
