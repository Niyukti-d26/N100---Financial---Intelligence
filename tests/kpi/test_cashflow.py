from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern,
)


def test_free_cash_flow_positive():
    assert free_cash_flow(500, -100) == 400


def test_free_cash_flow_negative():
    assert free_cash_flow(500, -700) == -200


def test_cfo_quality_high():
    assert cfo_quality_score(120, 100) == "High Quality"


def test_cfo_quality_moderate():
    assert cfo_quality_score(70, 100) == "Moderate"


def test_cfo_quality_accrual_risk():
    assert cfo_quality_score(20, 100) == "Accrual Risk"


def test_cfo_quality_pat_zero():
    assert cfo_quality_score(20, 0) is None


def test_capex_asset_light():
    pct, label = capex_intensity(-20, 1000)

    assert round(pct, 2) == 2.00
    assert label == "Asset Light"


def test_capex_moderate():
    pct, label = capex_intensity(-60, 1000)

    assert round(pct, 2) == 6.00
    assert label == "Moderate"


def test_capital_intensive():
    pct, label = capex_intensity(-200, 1000)

    assert round(pct, 2) == 20.00
    assert label == "Capital Intensive"


def test_fcf_conversion_rate():
    assert fcf_conversion_rate(250, 400) == 62.5


def test_capital_allocation_shareholder_returns():
    assert (
        capital_allocation_pattern(
            500,
            -100,
            -50,
            "High Quality",
        )
        == "Shareholder Returns"
    )


def test_capital_allocation_distress():
    assert (
        capital_allocation_pattern(
            -100,
            100,
            50,
        )
        == "Distress Signal"
    )