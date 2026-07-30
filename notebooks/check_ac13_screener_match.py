import requests
import pandas as pd

excel_df = pd.read_excel(
    "data/output/screener_output.xlsx"
)

api_df = pd.DataFrame(
    requests.get(
        "http://127.0.0.1:8000/api/v1/screener"
    ).json()
)

print(
    "Excel Rows =",
    len(excel_df)
)

print(
    "API Rows =",
    len(api_df)
)

excel_ids = set(
    excel_df["company_id"]
)

api_ids = set(
    api_df["company_id"]
)

print()
print(
    "Missing In API =",
    excel_ids - api_ids
)

print(
    "Missing In Excel =",
    api_ids - excel_ids
)