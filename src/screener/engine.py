import sqlite3
from pathlib import Path

import pandas as pd
import yaml

from src.config.settings import DATABASE_PATH

CONFIG_PATH = (
    Path(__file__).resolve().parent.parent
    / "config"
    / "screener_config.yaml"
)


class ScreenerEngine:

    def __init__(self, config_path=CONFIG_PATH):

        self.conn = sqlite3.connect(DATABASE_PATH)

        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

        self.df = self.load_data()
        self.calculate_composite_score()

    def load_data(self):

        ratios = pd.read_sql(
            """
            SELECT *
            FROM financial_ratios
            """,
            self.conn,
        )

        market = pd.read_sql(
            """
            SELECT
                company_id,
                year,
                market_cap_crore,
                pe_ratio,
                pb_ratio,
                dividend_yield_pct
            FROM market_cap
            """,
            self.conn,
        )

        pnl = pd.read_sql(
            """
            SELECT
                company_id,
                year,
                sales,
                net_profit
            FROM profitandloss
            """,
            self.conn,
        )

        sectors = pd.read_sql(
            """
            SELECT
                company_id,
                broad_sector
            FROM sectors
            """,
            self.conn,
        )

        df = ratios.merge(
            market,
            on=["company_id", "year"],
            how="left",
        )

        df = df.merge(
            pnl,
            on=["company_id", "year"],
            how="left",
        )

        df = df.merge(
            sectors,
            on="company_id",
            how="left",
        )

        latest_year = df["year"].max()

        df = df[
            df["year"] == latest_year
        ].copy()

        return df
    
    def get_data(self):
        return self.df.copy()
    
    def filter_roe(self):
        roe = self.config["filters"]["roe_min"]

        if roe is None:
            return self.df.copy()

        df = self.df.copy()

        df = df[
        df["return_on_equity_pct"] >= roe
    ]

        return df
    
    def filter_debt_to_equity(self):
        limit = self.config["filters"]["debt_to_equity_max"]

        if limit is None:
            return self.df.copy()

        df = self.df.copy()

        financials = df[df["broad_sector"] == "Financials"]

        non_financials = df[df["broad_sector"] != "Financials"]

        non_financials = non_financials[
            non_financials["debt_to_equity"] <= limit
    ]

        df = pd.concat(
        [financials, non_financials],
        ignore_index=True
    )

        return df
    
    def filter_free_cash_flow(self):
        limit = self.config["filters"]["free_cash_flow_min"]

        if limit is None:
         return self.df.copy()

        df = self.df.copy()

        df = df[
        df["free_cash_flow_cr"] >= limit
    ]

        return df

    def filter_revenue_cagr(self):
        limit = self.config["filters"]["revenue_cagr_5yr_min"]

        if limit is None:
            return self.df.copy()

        df = self.df.copy()

        df = df[
        df["revenue_cagr_5yr"] >= limit
    ]

        return df

    def filter_pat_cagr(self):
        limit = self.config["filters"]["pat_cagr_5yr_min"]

        if limit is None:
            return self.df.copy()

        df = self.df.copy()

        df = df[
        df["pat_cagr_5yr"] >= limit
    ]

        return df
    
    def filter_operating_profit_margin(self):
        limit = self.config["filters"]["operating_profit_margin_min"]

        if limit is None:
           return self.df.copy()

        df = self.df.copy()

        df = df[
        df["operating_profit_margin_pct"] >= limit
    ]

        return df
    
    def filter_pe_ratio(self):
        limit = self.config["filters"]["pe_ratio_max"]

        if limit is None:
            return self.df.copy()

        df = self.df.copy()

        df = df[
        df["pe_ratio"] <= limit
    ]

        return df
    
    def filter_pb_ratio(self):
        limit = self.config["filters"]["pb_ratio_max"]

        if limit is None:
            return self.df.copy()

        df = self.df.copy()

        df = df[
        df["pb_ratio"] <= limit
    ]

        return df
    
    def filter_dividend_yield(self):
        limit = self.config["filters"]["dividend_yield_min"]

        if limit is None:
            return self.df.copy()

        df = self.df.copy()

        df = df[
        df["dividend_yield_pct"] >= limit
    ]

        return df
    
    def filter_interest_coverage(self):
        limit = self.config["filters"]["interest_coverage_min"]
        if limit is None:
           return self.df.copy()

        df = self.df.copy()

        df["interest_coverage"] = df["interest_coverage"].replace(
        "Debt Free",
        float("inf")
    )

        df["interest_coverage"] = pd.to_numeric(
        df["interest_coverage"],
        errors="coerce"
    )

        df = df[
        df["interest_coverage"] >= limit
    ]

        return df
    
    def filter_market_cap(self):
        limit = self.config["filters"]["market_cap_min"]

        if limit is None:
            return self.df.copy()

        df = self.df.copy()

        df = df[
        df["market_cap_crore"] >= limit
    ]

        return df

    def filter_net_profit(self):
        limit = self.config["filters"]["net_profit_min"]

        if limit is None:
           return self.df.copy()

        df = self.df.copy()

        df = df[
        df["net_profit"] >= limit
    ]

        return df

    def filter_eps_cagr(self):
        limit = self.config["filters"]["eps_cagr_min"]

        if limit is None:
           return self.df.copy()

        df = self.df.copy()

        df = df[
        df["eps_cagr_5yr"] >= limit
    ]

        return df

    def filter_asset_turnover(self):
        limit = self.config["filters"]["asset_turnover_min"]

        if limit is None:
           return self.df.copy()

        df = self.df.copy()

        df = df[
        df["asset_turnover"] >= limit
    ]

        return df
    
    def filter_sales(self):
        limit = self.config["filters"]["sales_min"]

        if limit is None:
           return self.df.copy()

        df = self.df.copy()

        df = df[
        df["sales"] >= limit
    ]

        return df
    
    def winsorize_scale(self, series, inverse=False):
        
        series = pd.to_numeric(series, errors="coerce").fillna(0)

        p10 = series.quantile(0.10)
        p90 = series.quantile(0.90)

        series = series.clip(lower=p10, upper=p90)

        if p90 == p10:
          score = pd.Series(
            50,
            index=series.index,
            dtype=float
        )
        else:
           score = (
            (series - p10)
            /
            (p90 - p10)
        ) * 100

        if inverse:
          score = 100 - score

        return score.clip(0, 100)
    
    def calculate_composite_score(self):
        df = self.df.copy()

    # -----------------------------
    # Profitability (35%)
    # -----------------------------

        roe = self.winsorize_scale(
        df["return_on_equity_pct"]
    )

        roce = self.winsorize_scale(
        df["return_on_capital_employed_pct"]
    )

        npm = self.winsorize_scale(
        df["net_profit_margin_pct"]
    )

        profitability = (
        roe * 0.15 +
        roce * 0.10 +
        npm * 0.10
    )

    # -----------------------------
    # Cash Quality (30%)
    # -----------------------------

        fcf_conversion = self.winsorize_scale(
        df["fcf_conversion_pct"]
    )

        cfo = self.winsorize_scale(
        df["cash_from_operations_cr"]
    )

        fcf_positive = (
        df["free_cash_flow_cr"] > 0
    ).astype(int) * 100

        cash_quality = (
        fcf_conversion * 0.15 +
        cfo * 0.10 +
        fcf_positive * 0.05
    )

    # -----------------------------
    # Growth (20%)
    # -----------------------------

        revenue = self.winsorize_scale(
        df["revenue_cagr_5yr"]
    )

        pat = self.winsorize_scale(
        df["pat_cagr_5yr"]
    )

        growth = (
        revenue * 0.10 +
        pat * 0.10
    )

    # -----------------------------
    # Leverage (15%)
    # -----------------------------

        debt = self.winsorize_scale(
        df["debt_to_equity"],
        inverse=True
    )

        icr = self.winsorize_scale(
        df["interest_coverage"]
    )

        leverage = (
        debt * 0.10 +
        icr * 0.05
    )

    # -----------------------------
    # Final Score
    # -----------------------------

        df["composite_quality_score"] = (
        profitability +
        cash_quality +
        growth +
        leverage
    )

    # -----------------------------
    # Sector Relative Normalization
    # -----------------------------

        df["composite_quality_score"] = (
        df.groupby("broad_sector")[
            "composite_quality_score"
        ]
        .transform(
            lambda x: self.winsorize_scale(x)
        )
    )

        self.df = df

        return df
 
    def apply_filters(self, filters):
        df = self.df.copy()

        if "roe_min" in filters:
            df = df[df["return_on_equity_pct"] >= filters["roe_min"]]

        if "debt_to_equity_max" in filters:

            financials = df[df["broad_sector"] == "Financials"]

            others = df[df["broad_sector"] != "Financials"]

            others = others[
            others["debt_to_equity"] <= filters["debt_to_equity_max"]
        ]

            df = pd.concat([financials, others], ignore_index=True)

        if "free_cash_flow_min" in filters:
            df = df[
            df["free_cash_flow_cr"] >= filters["free_cash_flow_min"]
        ]

        if "revenue_cagr_5yr_min" in filters:
            df = df[
            df["revenue_cagr_5yr"] >= filters["revenue_cagr_5yr_min"]
        ]

        if "pat_cagr_5yr_min" in filters:
            df = df[
            df["pat_cagr_5yr"] >= filters["pat_cagr_5yr_min"]
        ]

        if "operating_profit_margin_min" in filters:
            df = df[
            df["operating_profit_margin_pct"] >= filters["operating_profit_margin_min"]
        ]

        if "pe_ratio_max" in filters:
            df = df[
            df["pe_ratio"] <= filters["pe_ratio_max"]
        ]

        if "pb_ratio_max" in filters:
            df = df[
            df["pb_ratio"] <= filters["pb_ratio_max"]
        ]

        if "dividend_yield_min" in filters:
            df = df[
            df["dividend_yield_pct"] >= filters["dividend_yield_min"]
        ]

        if "interest_coverage_min" in filters:

            df["interest_coverage"] = df["interest_coverage"].replace(
            "Debt Free",
            float("inf")
        )

            df["interest_coverage"] = pd.to_numeric(
            df["interest_coverage"],
            errors="coerce"
        )

            df = df[
            df["interest_coverage"] >= filters["interest_coverage_min"]
        ]

        if "market_cap_min" in filters:
            df = df[
            df["market_cap_crore"] >= filters["market_cap_min"]
        ]

        if "net_profit_min" in filters:
            df = df[
            df["net_profit"] >= filters["net_profit_min"]
        ]

        if "eps_cagr_min" in filters:
            df = df[
            df["eps_cagr_5yr"] >= filters["eps_cagr_min"]
        ]

        if "asset_turnover_min" in filters:
            df = df[
            df["asset_turnover"] >= filters["asset_turnover_min"]
        ]

        if "sales_min" in filters:
            df = df[
            df["sales"] >= filters["sales_min"]
        ]

        df = df.sort_values(
        "composite_quality_score",
        ascending=False
    )

        return df.reset_index(drop=True)
    
    def quality_compounder(self):
        
        filters = {

        "roe_min": 15,

        "debt_to_equity_max": 1,

        "free_cash_flow_min": 0,

        "revenue_cagr_5yr_min": 10

    }

        return self.apply_filters(filters)
    
    def value_pick(self):
        filters = {
        "pe_ratio_max": 20,
        "pb_ratio_max": 3,
        "debt_to_equity_max": 2,
        "dividend_yield_min": 1
    }

        return self.apply_filters(filters)
    
    def growth_accelerator(self):
        filters = {
        "pat_cagr_5yr_min": 20,
        "revenue_cagr_5yr_min": 15,
        "debt_to_equity_max": 2
    }

        return self.apply_filters(filters)

    def dividend_champion(self):
        filters = {
        "dividend_yield_min": 2,
        "free_cash_flow_min": 0
    }

        df = self.apply_filters(filters)

        df = df[
        df["dividend_payout_ratio_pct"] < 80
    ]

        return df
    
    def debt_free_blue_chip(self):
        filters = {
        "roe_min": 12,
        "sales_min": 5000
    }

        df = self.apply_filters(filters)

        df = df[
        df["debt_to_equity"] == 0
    ]

        return df
    
    def turnaround_watch(self):
        filters = {
        "free_cash_flow_min": 0
    }

        df = self.apply_filters(filters)

        df = df[
        df["revenue_cagr_5yr"] >= 10
    ]

        return df

    def close(self):
        self.conn.close()

    