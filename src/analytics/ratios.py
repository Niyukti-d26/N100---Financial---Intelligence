"""
Financial Ratio Engine

Sprint 2
Day 08

Contains reusable functions for calculating
profitability ratios.
"""
import math
def net_profit_margin(
    net_profit,
    sales,
):
    """
    Net Profit Margin

    Formula:
    Net Profit / Sales ×100
    """

    if sales == 0:
        return None

    return (net_profit / sales) * 100

def operating_profit_margin(
    operating_profit,
    sales,
):
    """
    Operating Profit Margin

    Formula:
    Operating Profit / Sales ×100
    """

    if sales == 0:
        return None

    return (operating_profit / sales) * 100

def opm_cross_check(
    calculated_opm,
    source_opm,
):
    """
    Returns True
    if difference >1%
    """

    if calculated_opm is None:
        return False

    if source_opm is None:
        return False

    return abs(calculated_opm - source_opm) > 1

def return_on_equity(
    net_profit,
    equity,
    reserves,
):
    """
    Return on Equity
    """

    denominator = equity + reserves

    if denominator <= 0:
        return None

    return (net_profit / denominator) * 100

def return_on_capital_employed(
    ebit,
    equity,
    reserves,
    borrowings,
):
    """
    Return on Capital Employed
    """

    capital = equity + reserves + borrowings

    if capital <= 0:
        return None

    return (ebit / capital) * 100

def return_on_assets(
    net_profit,
    total_assets,
):
    """
    Return on Assets
    """

    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100

def debt_to_equity(
    borrowings,
    equity,
    reserves,
):
    """
    Debt to Equity Ratio
    """

    if borrowings == 0:
        return 0

    denominator = equity + reserves

    if denominator <= 0:
        return None

    return borrowings / denominator

def high_leverage_flag(
    debt_to_equity_ratio,
    broad_sector,
):
    """
    Returns True
    if company has high leverage.
    """

    if debt_to_equity_ratio is None:
        return False

    if broad_sector == "Financials":
        return False

    return debt_to_equity_ratio > 5

def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest,
):
    """
    Interest Coverage Ratio
    """

    if interest == 0:
        return None

    return (
        operating_profit +
        other_income
    ) / interest

def interest_coverage_label(
    interest,
):
    """
    Returns Debt Free
    if company has no interest.
    """

    if interest == 0:
        return "Debt Free"

    return ""

def icr_warning(
    interest_coverage,
):
    """
    Warning flag
    """

    if interest_coverage is None:
        return False

    return interest_coverage < 1.5

def net_debt(
    borrowings,
    investments,
):
    """
    Net Debt
    """

    return borrowings - investments

def asset_turnover(
    sales,
    total_assets,
):
    """
    Asset Turnover Ratio
    """

    if total_assets == 0:
        return None

    return sales / total_assets

