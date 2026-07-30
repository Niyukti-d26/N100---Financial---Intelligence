

def free_cash_flow(
    operating_activity,
    investing_activity,
):
    """Function: free_cash_flow"""
    return operating_activity + investing_activity


def cfo_quality_score(cfo, pat):
    """Function: cfo_quality_score"""
    if pat == 0:
        return None

    ratio = cfo / pat

    if ratio > 1:
        return "High Quality"

    elif ratio >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(
    investing_activity,
    sales,
):
    """Function: capex_intensity"""
    if sales == 0:
        return None, None

    pct = abs(investing_activity) / sales * 100

    if pct < 3:
        label = "Asset Light"

    elif pct <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return round(pct, 2), label


def fcf_conversion_rate(
    free_cash_flow,
    operating_profit,
):
    """Function: fcf_conversion_rate"""
    if operating_profit == 0:
        return None

    return round(
        free_cash_flow / operating_profit * 100,
        2,
    )


def capital_allocation_pattern(
    cfo,
    cfi,
    cff,
    quality=None,
):
    """Function: capital_allocation_pattern"""
    pattern = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-",
    )

    mapping = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "+", "-"): "Liquidating Assets",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "-"): "Pre-Revenue",
        ("+", "-", "+"): "Mixed",
    }

    label = mapping.get(pattern, "Unknown")

    if pattern == ("+", "-", "-") and quality == "High Quality":
        label = "Shareholder Returns"

    return label
