from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    opm_cross_check,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    interest_coverage_label,
    icr_warning,
    net_debt,
    asset_turnover,
)

def test_net_profit_margin():

    assert net_profit_margin(200,1000)==20

def test_zero_sales():

    assert net_profit_margin(200,0) is None

def test_operating_margin():

    assert operating_profit_margin(300,1000)==30

def test_opm_cross_check():

    calculated=30
    source=28

    assert opm_cross_check(calculated,source)

def test_return_on_equity():

    assert return_on_equity(
        200,
        500,
        500,
    )==20

def test_negative_equity():

    assert return_on_equity(
        200,
        -100,
        -50,
    ) is None

def test_roce():

    assert return_on_capital_employed(
        400,
        500,
        500,
        1000,
    )==20

def test_roa():

    assert return_on_assets(
        300,
        1000,
    )==30

def test_debt_to_equity():

    assert debt_to_equity(
        100,
        500,
        500,
    ) == 0.1

def test_debt_free():

    assert debt_to_equity(
        0,
        500,
        500,
    ) == 0

def test_interest_coverage():

    assert interest_coverage_ratio(
        500,
        100,
        100,
    ) == 6

def test_interest_zero():

    assert interest_coverage_ratio(
        500,
        100,
        0,
    ) is None

def test_debt_free_label():

    assert interest_coverage_label(
        0,
    ) == "Debt Free"

def test_high_leverage():

    assert high_leverage_flag(
        6,
        "Technology",
    )

def test_icr_warning():

    assert icr_warning(
        1.2,
    )

def test_asset_turnover():

    assert asset_turnover(
        1000,
        500,
    ) == 2

