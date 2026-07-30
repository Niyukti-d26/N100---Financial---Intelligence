from pathlib import Path

import pandas as pd

from src.screener.engine import ScreenerEngine

engine = ScreenerEngine()

screeners = {
    "Quality Compounder": engine.quality_compounder(),
    "Value Pick": engine.value_pick(),
    "Growth Accelerator": engine.growth_accelerator(),
    "Dividend Champion": engine.dividend_champion(),
    "Debt Free Blue Chip": engine.debt_free_blue_chip(),
    "Turnaround Watch": engine.turnaround_watch(),
}

output_path = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "output"
    / "screener_output.xlsx"
)

with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

    for sheet_name, df in screeners.items():

        df.to_excel(
            writer,
            sheet_name=sheet_name[:31],
            index=False,
        )

engine.close()

print()

print("====================================")
print(" Screener Output Generated")
print("====================================")
print(output_path)
