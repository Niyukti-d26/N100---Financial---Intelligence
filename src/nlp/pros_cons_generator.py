import sqlite3
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DB_PATH = ROOT / "db" / "nifty100.db"

OUTPUT_DIR = ROOT / "data" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


conn = sqlite3.connect(DB_PATH)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

pl = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

cf = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

conn.close()


records = []


def add_record(
    company,
    signal_type,
    rule_id,
    text,
    confidence
):
    records.append(
        {
            "company_id": company,
            "type": signal_type,
            "rule_id": rule_id,
            "text": text,
            "confidence_pct": confidence
        }
    )


for company in companies["id"]:

    r = ratios[
        ratios["company_id"] == company
    ].copy()

    r = r.dropna(subset=["year"])

    if r.empty:
        continue

    r = r.sort_values("year")

    latest = r.iloc[-1]

    company_pl = pl[
        pl["company_id"] == company
    ].copy()

    company_pl = company_pl.dropna(
        subset=["year"]
    )

    company_pl = company_pl.sort_values(
        "year"
    )

    # ======================
    # PRO RULES
    # ======================

    if len(r) >= 3:

        last3 = r.tail(3)

        if (
            last3[
                "return_on_equity_pct"
            ] > 20
        ).all():

            add_record(
                company,
                "pro",
                "PRO_01",
                "Consistently high return on equity above 20% demonstrates exceptional capital efficiency",
                95
            )

    if len(r) >= 5:

        last5 = r.tail(5)

        if (
            last5[
                "free_cash_flow_cr"
            ] > 0
        ).all():

            add_record(
                company,
                "pro",
                "PRO_02",
                "Strong free cash flow generation over 5 years signals healthy business fundamentals",
                90
            )

    if latest["debt_to_equity"] == 0:

        add_record(
            company,
            "pro",
            "PRO_03",
            "Debt-free balance sheet provides financial flexibility and eliminates interest burden",
            95
        )

    if (
        latest["revenue_cagr_5yr"]
        > 15
    ):

        add_record(
            company,
            "pro",
            "PRO_04",
            "Revenue growing at above 15% CAGR over 5 years reflects strong business momentum",
            85
        )

    if (
        latest[
            "operating_profit_margin_pct"
        ] > 25
    ):

        add_record(
            company,
            "pro",
            "PRO_05",
            "Operating profit margin above 25% indicates strong pricing power and cost discipline",
            85
        )

    if (
        latest["pat_cagr_5yr"]
        > 20
    ):

        add_record(
            company,
            "pro",
            "PRO_06",
            "Net profit compounding at above 20% over 5 years creates significant shareholder value",
            90
        )

    if (
        latest["interest_coverage"]
        > 10
        or latest["debt_to_equity"] == 0
    ):

        add_record(
            company,
            "pro",
            "PRO_07",
            "Very high interest coverage ratio reflects negligible financial stress from debt servicing",
            85
        )

    if (
        latest[
            "dividend_payout_ratio_pct"
        ] > 2
        and latest[
            "free_cash_flow_cr"
        ] > 0
    ):

        add_record(
            company,
            "pro",
            "PRO_08",
            "Consistent dividend backed by positive free cash flow",
            80
        )

    if (
        latest["eps_cagr_5yr"]
        > 15
    ):

        add_record(
            company,
            "pro",
            "PRO_09",
            "EPS growing above 15% CAGR indicates strong earnings quality",
            85
        )

    if len(r) >= 3:

        last3 = r.tail(3)

        if (
            last3[
                "return_on_equity_pct"
            ].is_monotonic_increasing
        ):

            add_record(
                company,
                "pro",
                "PRO_10",
                "Return on equity improving for 3 consecutive years",
                80
            )

    if (
        latest["pat_cagr_5yr"]
        >
        latest["revenue_cagr_5yr"]
    ):

        add_record(
            company,
            "pro",
            "PRO_11",
            "Revenue growing slower than profits shows improving operating leverage",
            80
        )

    if len(r) >= 3:

        last3 = r.tail(3)

        if (
            last3[
                "debt_to_equity"
            ].is_monotonic_decreasing
        ):

            add_record(
                company,
                "pro",
                "PRO_12",
                "Debt levels declining over time indicate strengthening balance sheet quality",
                80
            )

    # ======================
    # CON RULES
    # ======================

    if latest["debt_to_equity"] > 2:

        add_record(
            company,
            "con",
            "CON_01",
            f"Debt-to-equity ratio of {latest['debt_to_equity']:.2f} is elevated and warrants monitoring",
            90
        )

    if len(r) >= 3:

        last3 = r.tail(3)

        if (
            last3[
                "free_cash_flow_cr"
            ] < 0
        ).all():

            add_record(
                company,
                "con",
                "CON_02",
                "Free cash flow negative for 3 consecutive years raises concern about cash generation quality",
                90
            )

    if len(r) >= 3:

        last3 = r.tail(3)

        if (
            last3[
                "operating_profit_margin_pct"
            ].is_monotonic_decreasing
        ):

            add_record(
                company,
                "con",
                "CON_03",
                "Operating margins declining for 3 consecutive years",
                85
            )

    if (
        latest[
            "interest_coverage"
        ] < 1.5
    ):

        add_record(
            company,
            "con",
            "CON_04",
            "Interest coverage ratio below 1.5x indicates debt servicing risk",
            95
        )

    if (
        latest["revenue_cagr_5yr"]
        < 5
    ):

        add_record(
            company,
            "con",
            "CON_05",
            "Revenue growth below 5% over 5 years suggests limited business momentum",
            85
        )

    if (
        latest[
            "return_on_capital_employed_pct"
        ] < 10
    ):

        add_record(
            company,
            "con",
            "CON_06",
            "ROCE below 10% suggests weak capital efficiency",
            85
        )


output = pd.DataFrame(records)

output = output[
    output["confidence_pct"] > 60
]


# Guarantee every company has at least 1 pro and 1 con

for company in companies["id"]:

    subset = output[
        output["company_id"] == company
    ]

    if not (
        subset["type"] == "pro"
    ).any():

        output.loc[len(output)] = [
            company,
            "pro",
            "DEFAULT_PRO",
            "Business maintains operational continuity",
            65
        ]

    if not (
        subset["type"] == "con"
    ).any():

        output.loc[len(output)] = [
            company,
            "con",
            "DEFAULT_CON",
            "Limited strong negative signals available in current dataset",
            65
        ]


output.to_csv(
    OUTPUT_DIR /
    "pros_cons_generated.csv",
    index=False
)

print(
    "Generated:",
    len(output),
    "records"
)