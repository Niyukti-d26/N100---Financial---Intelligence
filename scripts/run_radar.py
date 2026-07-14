from src.radar.engine import RadarEngine

engine = RadarEngine()

companies = engine.df["company_id"].tolist()

for company in companies:
    try:
        path = engine.plot_radar(company)
        print(f"Generated: {path}")
    except Exception as e:
        print(f"Failed: {company} -> {e}")

engine.close()

print("Done!")