from src.peer_engine.engine import PeerEngine


def test_peer_engine_load():

    engine = PeerEngine()

    df = engine.get_data()

    assert len(df) > 0

    required_columns = [
        "company_id",
        "peer_group_name",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "market_cap_crore",
        "pe_ratio",
        "pb_ratio",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "asset_turnover",
    ]

    for column in required_columns:
        assert column in df.columns

    engine.close()
