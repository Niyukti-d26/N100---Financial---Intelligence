import re
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = ROOT / "db" / "nifty100.db"
OUTPUT_DIR = ROOT / "data" / "output"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

PATTERN = r"(\d+)\s*Years?:?\s*(-?[\d.]+)%"

def parse_metric(company_id, metric_name, text):

    if pd.isna(text):
        return None

    text = str(text).strip()

    match = re.search(
        r"(\d+)\s*Years?:?\s*(-?[\d.]+)%",
        text
    )

    if match:

        return {
            "company_id": company_id,
            "metric_type": metric_name,
            "period_years": int(match.group(1)),
            "value_pct": float(match.group(2))
        }

    ttm_match = re.search(
        r"TTM:?\s*(-?[\d.]+)%",
        text
    )

    if ttm_match:

        return {
            "company_id": company_id,
            "metric_type": metric_name,
            "period_years": 0,
            "value_pct": float(ttm_match.group(1))
        }

    last_year_match = re.search(
        r"Last Year:?\s*(-?[\d.]+)%",
        text
    )

    if last_year_match:

        return {
            "company_id": company_id,
            "metric_type": metric_name,
            "period_years": 1,
            "value_pct": float(last_year_match.group(1))
        }

    return None


def run_parser():

    conn = sqlite3.connect(DATABASE_PATH)

    analysis = pd.read_sql(
        "SELECT * FROM analysis",
        conn
    )

    parsed_records = []
    failures = []

    metric_columns = [
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe"
    ]

    for _, row in analysis.iterrows():

        company_id = row["company_id"]

        for metric in metric_columns:

            result = parse_metric(
                company_id,
                metric,
                row[metric]
            )

            if result:
                parsed_records.append(result)

            else:
                failures.append({
                    "company_id": company_id,
                    "metric_type": metric,
                    "raw_text": row[metric]
                })

    parsed_df = pd.DataFrame(parsed_records)

    failures_df = pd.DataFrame(failures)

    parsed_df.to_csv(
        OUTPUT_DIR / "analysis_parsed.csv",
        index=False
    )

    failures_df.to_csv(
        OUTPUT_DIR / "parse_failures.csv",
        index=False
    )

    conn.close()

    print(
        f"Parsed rows: {len(parsed_df)}"
    )

    print(
        f"Failures: {len(failures_df)}"
    )


if __name__ == "__main__":
    run_parser()