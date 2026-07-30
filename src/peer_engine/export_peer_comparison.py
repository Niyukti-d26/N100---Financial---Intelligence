from pathlib import Path

import pandas as pd

from src.peer_engine.engine import PeerEngine

engine = PeerEngine()

df = engine.generate_peer_comparison()
df = df[df["peer_group_name"].notna()].copy()

output_path = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "output"
    / "peer_comparison.xlsx"
)

with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

    df.to_excel(
        writer,
        sheet_name="Peer Comparison",
        index=False,
    )

engine.close()

print()
print("=" * 45)
print("Peer Comparison Exported Successfully")
print("=" * 45)
print(output_path)
