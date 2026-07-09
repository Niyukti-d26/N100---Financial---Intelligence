from src.screener.engine import ScreenerEngine


def test_engine_load():

    engine = ScreenerEngine()

    df = engine.get_data()

    assert len(df) > 0

    required_columns = [
        "company_id",
        "year",
        "return_on_equity_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "operating_profit_margin_pct",
        "interest_coverage",
        "asset_turnover",
        "market_cap_crore",
        "pe_ratio",
        "pb_ratio",
        "dividend_yield_pct",
        "sales",
        "net_profit",
        "composite_quality_score"
    ]

    for column in required_columns:
        assert column in df.columns

def test_roe_filter():
        engine = ScreenerEngine()

        df = engine.filter_roe()

        assert len(df) > 0

        assert (
        df["return_on_equity_pct"] >= 15
        ).all()

def test_debt_to_equity_filter():

    engine = ScreenerEngine()

    df = engine.filter_debt_to_equity()

    non_financials = df[
        df["broad_sector"] != "Financials"
    ]

    assert (
        non_financials["debt_to_equity"] <= 1
    ).all()

def test_free_cash_flow_filter():

    engine = ScreenerEngine()

    df = engine.filter_free_cash_flow()

    assert len(df) > 0

    assert (
        df["free_cash_flow_cr"] >= 0
    ).all()

def test_revenue_cagr_filter():

    engine = ScreenerEngine()

    df = engine.filter_revenue_cagr()

    assert len(df) > 0

    assert (
        df["revenue_cagr_5yr"] >= 10
    ).all()

def test_pat_cagr_filter():

    engine = ScreenerEngine()

    df = engine.filter_pat_cagr()

    assert len(df) > 0

    assert (
        df["pat_cagr_5yr"] >= 10
    ).all()

def test_operating_profit_margin_filter():

    engine = ScreenerEngine()

    df = engine.filter_operating_profit_margin()

    assert len(df) > 0

    assert (
        df["operating_profit_margin_pct"] >= 15
    ).all()

def test_pe_ratio_filter():

    engine = ScreenerEngine()

    df = engine.filter_pe_ratio()

    assert len(df) > 0

    assert (
        df["pe_ratio"] <= 20
    ).all()

def test_pb_ratio_filter():

    engine = ScreenerEngine()

    df = engine.filter_pb_ratio()

    assert len(df) > 0

    assert (
        df["pb_ratio"] <= 3
    ).all()

def test_dividend_yield_filter():

    engine = ScreenerEngine()

    df = engine.filter_dividend_yield()

    assert len(df) > 0

    assert (
        df["dividend_yield_pct"] >= 1
    ).all()

def test_interest_coverage_filter():

    engine = ScreenerEngine()

    df = engine.filter_interest_coverage()

    assert len(df) > 0

    assert (
        df["interest_coverage"] >= 3
    ).all()

def test_market_cap_filter():

    engine = ScreenerEngine()

    df = engine.filter_market_cap()

    assert len(df) > 0

    assert (
        df["market_cap_crore"] >= 10000
    ).all()

def test_net_profit_filter():

    engine = ScreenerEngine()

    df = engine.filter_net_profit()

    assert len(df) > 0

    assert (
        df["net_profit"] >= 1000
    ).all()

def test_eps_cagr_filter():

    engine = ScreenerEngine()

    df = engine.filter_eps_cagr()

    assert len(df) > 0

    assert (
        df["eps_cagr_5yr"] >= 10
    ).all()

def test_asset_turnover_filter():

    engine = ScreenerEngine()

    df = engine.filter_asset_turnover()

    assert len(df) > 0

    assert (
        df["asset_turnover"] >= 0.5
    ).all()

def test_sales_filter():

    engine = ScreenerEngine()

    df = engine.filter_sales()

    assert len(df) > 0

    assert (
        df["sales"] >= 5000
    ).all()