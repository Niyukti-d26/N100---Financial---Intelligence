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

