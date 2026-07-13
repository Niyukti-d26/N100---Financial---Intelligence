import pandas as pd

from src.peer_engine.engine import PeerEngine


def test_peer_percentiles_table():

    engine = PeerEngine()

    engine.save_peer_percentiles()

    df = pd.read_sql(
        "SELECT * FROM peer_percentiles",
        engine.conn,
    )

    assert len(df) > 0

    expected_columns = [
        "company_id",
        "peer_group_name",
        "metric",
        "value",
        "percentile_rank",
        "year",
    ]

    for column in expected_columns:
        assert column in df.columns