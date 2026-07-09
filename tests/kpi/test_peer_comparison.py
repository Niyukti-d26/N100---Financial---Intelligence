from src.peer_engine.engine import PeerEngine


def test_generate_peer_comparison():

    engine = PeerEngine()

    df = engine.generate_peer_comparison()

    expected_columns = [
        "roe_rank",
        "roe_percentile",
        "roce_rank",
        "roce_percentile",
        "marketcap_rank",
        "marketcap_percentile",
        "pe_rank",
        "pe_percentile",
        "pb_rank",
        "pb_percentile",
        "revenue_rank",
        "revenue_percentile",
        "pat_rank",
        "pat_percentile",
        "eps_rank",
        "eps_percentile",
        "asset_turnover_rank",
        "asset_turnover_percentile",
    ]

    for column in expected_columns:
        assert column in df.columns

    engine.close()