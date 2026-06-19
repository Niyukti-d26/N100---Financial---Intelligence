import pandas as pd

from src.config.settings import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    HEADER_ROWS,
)

from src.etl.normaliser import normalize
from src.utils.logger import logger


def clean_columns(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("%", "pct", regex=False)
        .str.replace("/", "_", regex=False)
    )

    return df


def load_file(filename):

    filepath = RAW_DATA_DIR / filename

    header = HEADER_ROWS.get(filename, 0)

    logger.info(f"Loading {filename}")

    df = pd.read_excel(filepath, header=header)

    df = clean_columns(df)

    df = normalize(df)

    return df


def save_processed(df, filename):

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_file = PROCESSED_DATA_DIR / f"{filename}.csv"

    df.to_csv(output_file, index=False)


def load_all():

    datasets = {}

    for file in RAW_DATA_DIR.glob("*.xlsx"):

        df = load_file(file.name)

        datasets[file.stem] = df

        save_processed(df, file.stem)

        logger.info(f"{file.name} loaded successfully")

    return datasets


if __name__ == "__main__":

    datasets = load_all()

    print("\n")

    print("=" * 80)
    print("DATASETS LOADED")
    print("=" * 80)

    for name, df in datasets.items():

        print(
            f"{name:<25}"
            f"Rows: {df.shape[0]:5}"
            f" Columns: {df.shape[1]:2}"
        )