from src.radar.engine import RadarEngine


def test_radar_engine():

    engine = RadarEngine()

    df = engine.df

    assert len(df) > 0