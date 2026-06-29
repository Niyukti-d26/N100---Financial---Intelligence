from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    opm_cross_check,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
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