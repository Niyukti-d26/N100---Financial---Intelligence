from src.peer_engine.engine import PeerEngine


def test_metric_ranking():

    engine = PeerEngine()

    metrics = [
        ("return_on_equity_pct", "roe_rank", "roe_percentile"),
        ("return_on_capital_employed_pct", "roce_rank", "roce_percentile"),
        ("market_cap_crore", "marketcap_rank", "marketcap_percentile"),
        ("pe_ratio", "pe_rank", "pe_percentile"),
        ("pb_ratio", "pb_rank", "pb_percentile"),
        ("revenue_cagr_5yr", "revenue_rank", "revenue_percentile"),
        ("pat_cagr_5yr", "pat_rank", "pat_percentile"),
        ("eps_cagr_5yr", "eps_rank", "eps_percentile"),
        ("asset_turnover", "asset_turnover_rank", "asset_turnover_percentile"),
    ]

    for metric, rank, percentile in metrics:

        df = engine.rank_metric(metric, rank)

        assert rank in df.columns

        assert df[rank].dropna().min() == 1

        df = engine.percentile_metric(metric, percentile)

        assert percentile in df.columns

        assert (
            df[percentile].dropna().between(0, 100)
        ).all()

    engine.close()