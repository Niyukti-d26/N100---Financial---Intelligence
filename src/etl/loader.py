import sqlite3
import pandas as pd

from src.config.settings import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    OUTPUT_DIR,
    DATABASE_PATH,
    SCHEMA_PATH,
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

    print("\n" + "=" * 70)
    print(filename)
    print("Rows before cleaning :", len(df))
    print("Duplicate rows before cleaning :", df.duplicated().sum())

    df = clean_columns(df)

    print("Duplicate rows after clean_columns :", df.duplicated().sum())

    df = normalize(df)

    print("Duplicate rows after normalize :", df.duplicated().sum())

    return df


def save_processed(df, filename):

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_file = PROCESSED_DATA_DIR / f"{filename}.csv"

    df.to_csv(output_file, index=False)

def create_database():

    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()

    conn = sqlite3.connect(DATABASE_PATH)

    conn.execute("PRAGMA foreign_keys = ON;")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        conn.executescript(file.read())

    print("=" * 80)
    print("SQLite Database Created Successfully")
    print("=" * 80)

    return conn

def filter_foreign_keys(df, companies_df, table):

    if "company_id" not in df.columns:
        return df, 0

    valid_ids = set(companies_df["id"])

    invalid = df[~df["company_id"].isin(valid_ids)]

    valid = df[df["company_id"].isin(valid_ids)]

    if len(invalid) > 0:

        print(
            f"{table:<20}"
            f"Rejected {len(invalid)} rows (Invalid company_id)"
        )

    return valid, len(invalid)

def load_into_database(conn, datasets):

    load_audit = []

    load_order = [
    "companies",
    "sectors",
    "analysis",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "documents",
    "prosandcons",
    "financial_ratios",
    "market_cap",
    "peer_groups",
    "stock_prices",
    ]

    for table in load_order:
        if table not in datasets:
            continue

        df = datasets[table]

        rejected = 0

        if table != "companies":
            df, rejected = filter_foreign_keys(
                df,
                datasets["companies"],
                table,
            )

        try:
            df.to_sql(
                table,
                conn,
                if_exists="append",
                index=False,
            )

            conn.commit()

            print(
                conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            )

            print(f"{table:<20} Loaded {len(df)} rows")

        

        except Exception as e:
            import traceback

            print("\n" + "=" * 80)
            print(f"FAILED TABLE : {table}")
            print("=" * 80)

            print("ERROR TYPE:", type(e))
            print("ERROR:", e)

            traceback.print_exc()

            break

        load_audit.append(
            {
                "table": table,
                "rows_loaded": len(df),
                "rows_rejected": rejected,
                "status": "SUCCESS",
            }
        )


    audit_df = pd.DataFrame(load_audit)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    audit_df.to_csv(
        OUTPUT_DIR / "load_audit.csv",
        index=False,
    )

    print("\n")
    print("=" * 80)
    print("LOAD AUDIT GENERATED")
    print("=" * 80)

    return audit_df

def check_foreign_keys(conn):

    result = conn.execute(
        "PRAGMA foreign_key_check;"
    ).fetchall()

    print("\n")
    print("=" * 80)

    if len(result) == 0:

        print("Foreign Key Check Passed")

    else:

        print("Foreign Key Violations Found")

        for row in result:
            print(row)

    print("=" * 80)

def load_all():

    datasets = {}

    for file in RAW_DATA_DIR.glob("*.xlsx"):

        df = load_file(file.name)

        datasets[file.stem] = df

        save_processed(df, file.stem)

        logger.info(f"{file.name} loaded successfully")

    return datasets

def print_database_summary(conn):

    print("\n")
    print("=" * 80)
    print("DATABASE SUMMARY")
    print("=" * 80)

    tables = [
        "companies",
        "analysis",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "documents",
        "prosandcons",
        "financial_ratios",
        "market_cap",
        "peer_groups",
        "sectors",
        "stock_prices",
    ]

    for table in tables:

        count = conn.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f"{table:<20}{count}")


if __name__ == "__main__":

    # ============================================================
    # STEP 1 : Load Excel Files
    # ============================================================

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

    # ============================================================
    # STEP 2 : Create SQLite Database
    # ============================================================

    conn = create_database()

    # ============================================================
    # STEP 3 : Load Tables into SQLite
    # ============================================================

    load_into_database(
        conn,
        datasets,
    )

    # ============================================================
    # STEP 4 : Check Foreign Keys
    # ============================================================

    check_foreign_keys(conn)
    print_database_summary(conn)

    conn.commit()

    conn.close()

    print("\n")
    print("=" * 80)
    print("DATABASE LOAD COMPLETED")
    print("=" * 80)