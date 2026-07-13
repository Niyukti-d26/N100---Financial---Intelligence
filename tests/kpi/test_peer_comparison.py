from src.peer_engine.engine import PeerEngine


def test_generate_peer_comparison():

    engine = PeerEngine()

    df = engine.generate_peer_comparison()

    expected_columns = [
    "roe_rank",
    "roe_percentile",

    "roce_rank",
    "roce_percentile",

    "npm_rank",
    "npm_percentile",

    "de_rank",
    "de_percentile",

    "fcf_rank",
    "fcf_percentile",

    "revenue_rank",
    "revenue_percentile",

    "pat_rank",
    "pat_percentile",

    "eps_rank",
    "eps_percentile",

    "icr_rank",
    "icr_percentile",

    "asset_turnover_rank",
    "asset_turnover_percentile",
]
    for column in expected_columns:
        assert column in df.columns

    engine.close()