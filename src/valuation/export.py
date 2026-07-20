from src.valuation.engine import ValuationEngine

engine = ValuationEngine()

df = engine.generate_valuation()

output_cols = [
    "company_id",
    "year",
    "market_cap_crore",
    "pe_ratio",
    "pb_ratio",
    "dividend_yield_pct",
    "net_cash_flow",
    "fcf_yield_pct",
    "valuation_label"
]

df[output_cols].to_excel(
    "valuation_summary.xlsx",
    index=False
)

print(
    "valuation_summary.xlsx generated successfully"
)

engine.close()