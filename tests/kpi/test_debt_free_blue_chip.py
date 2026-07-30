from src.screener.engine import ScreenerEngine


def test_debt_free_blue_chip():

    engine = ScreenerEngine()

    df = engine.debt_free_blue_chip()

    assert len(df) > 0

    assert (df["debt_to_equity"] == 0).all()
    assert (df["return_on_equity_pct"] >= 12).all()
    assert (df["sales"] >= 5000).all()
