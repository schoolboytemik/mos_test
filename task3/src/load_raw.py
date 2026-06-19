from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


ROOT = Path(__file__).resolve().parents[1]

CLEANED = ROOT / "data" / "cleaned"

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@postgres:5432/mos"
)


FILES = {
    "customers.csv": "customers",
    "products.csv": "products",
    "orders.csv": "orders",
    "payments.csv": "payments",
    "events.csv": "events",
}



for filename, table in FILES.items():

    path = CLEANED / filename

    print(f"Loading {filename} -> raw.{table}")

    try:
        df = pd.read_csv(path)

        df["source_file"] = filename

        df.to_sql(
            name=table,
            con=engine,
            schema="raw",
            if_exists="append",
            index=False
        )

        print(f"SUCCESS: {table}")

    except Exception as e:
        print(f"FAILED: {table}")
        print(e)
        raise

print("Done")