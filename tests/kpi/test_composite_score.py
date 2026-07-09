from src.screener.engine import ScreenerEngine


def test_composite_score():

    engine = ScreenerEngine()

    df = engine.get_data()

    assert "composite_quality_score" in df.columns

    assert df["composite_quality_score"].notna().all()

    engine.close()