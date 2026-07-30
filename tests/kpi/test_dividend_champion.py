from src.screener.engine import ScreenerEngine


def test_dividend_champion():

    engine = ScreenerEngine()

    df = engine.dividend_champion()

    assert len(df) > 0

    assert (df["dividend_yield_pct"] >= 2).all()
    assert (df["free_cash_flow_cr"] >= 0).all()
    assert (df["dividend_payout_ratio_pct"] < 80).all()
