from src.screener.engine import ScreenerEngine


def test_all_screeners():

    engine = ScreenerEngine()

    screeners = {
        "Quality Compounder": engine.quality_compounder(),
        "Value Pick": engine.value_pick(),
        "Growth Accelerator": engine.growth_accelerator(),
        "Dividend Champion": engine.dividend_champion(),
        "Debt Free Blue Chip": engine.debt_free_blue_chip(),
        "Turnaround Watch": engine.turnaround_watch(),
    }

    for name, df in screeners.items():

        company_count = df["company_id"].nunique()

        print(f"\n{name}")
        print(f"Company Count: {company_count}")

        print(
            df[
                [
                    "company_id",
                    "year",
                    "composite_quality_score",
                ]
            ].head(10)
        )

        assert company_count > 0

    engine.close()
