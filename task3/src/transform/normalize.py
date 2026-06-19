import pandas as pd
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA = ROOT / "data"
OUT = DATA / "cleaned"

OUT.mkdir(exist_ok=True)

log = []


def save_problem(dataset, row, reason):
    log.append(f"{dataset}: {reason} -> {row}")


def clean_text(series):
    return (
        series.astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )


def clean_strings(df):
    for col in df.select_dtypes(include="object").columns:
        df[col] = clean_text(df[col])
    return df


# ------------------
# CUSTOMERS
# ------------------

customers = pd.read_csv(DATA / "customers.csv")

customers = clean_strings(customers)

customers["full_name"] = customers["full_name"].str.title()

customers["phone"] = customers["phone"].replace("UNKNOWN", pd.NA)

customers["created_at"] = pd.to_datetime(
    customers["created_at"],
    errors="coerce"
)

bad_dates = customers["created_at"].isna()

for _, row in customers[bad_dates].iterrows():
    save_problem(
        "customers",
        row.to_dict(),
        "invalid created_at"
    )

customers.to_csv(
    OUT / "customers.csv",
    index=False
)


# ------------------
# EVENTS XML
# ------------------

root = ET.parse(DATA / "events.xml").getroot()

rows = []

for event in root.findall("event"):
    rows.append({
        child.tag: child.text
        for child in event
    })

events = pd.DataFrame(rows)

events = clean_strings(events)

events["event_timestamp"] = pd.to_datetime(
    events["event_timestamp"],
    errors="coerce"
)

bad_dates = events["event_timestamp"].isna()

for _, row in events[bad_dates].iterrows():
    save_problem(
        "events",
        row.to_dict(),
        "invalid event_timestamp"
    )

events["event_id"] = pd.to_numeric(
    events["event_id"],
    errors="coerce"
)

events["customer_id"] = pd.to_numeric(
    events["customer_id"],
    errors="coerce"
)

events["product_id"] = pd.to_numeric(
    events["product_id"],
    errors="coerce"
)

bad_ids = (
    events["event_id"].isna()
    | events["customer_id"].isna()
    | events["product_id"].isna()
)

for _, row in events[bad_ids].iterrows():
    save_problem(
        "events",
        row.to_dict(),
        "invalid id"
    )

events.to_csv(
    OUT / "events.csv",
    index=False
)


# ------------------
# ORDERS JSON
# ------------------

with open(DATA / "orders.json", encoding="utf-8") as f:
    orders = pd.DataFrame(json.load(f))

orders = clean_strings(orders)

orders["order_timestamp"] = pd.to_datetime(
    orders["order_timestamp"],
    errors="coerce"
)

orders["unit_price"] = pd.to_numeric(
    orders["unit_price"],
    errors="coerce"
)

bad_dates = orders["order_timestamp"].isna()

for _, row in orders[bad_dates].iterrows():
    save_problem(
        "orders",
        row.to_dict(),
        "invalid order_timestamp"
    )

bad_prices = orders["unit_price"].isna()

for _, row in orders[bad_prices].iterrows():
    save_problem(
        "orders",
        row.to_dict(),
        "invalid unit_price"
    )

orders.to_csv(
    OUT / "orders.csv",
    index=False
)


# ------------------
# PAYMENTS
# ------------------

payments = pd.read_csv(
    DATA / "payments.csv",
    sep="^"
)

payments = clean_strings(payments)

payments["amount"] = pd.to_numeric(
    payments["amount"],
    errors="coerce"
)

payments["payment_timestamp"] = pd.to_datetime(
    payments["payment_timestamp"],
    errors="coerce"
)

bad_amounts = payments["amount"].isna()

for _, row in payments[bad_amounts].iterrows():
    save_problem(
        "payments",
        row.to_dict(),
        "invalid amount"
    )

bad_dates = payments["payment_timestamp"].isna()

for _, row in payments[bad_dates].iterrows():
    save_problem(
        "payments",
        row.to_dict(),
        "invalid payment_timestamp"
    )

payments.to_csv(
    OUT / "payments.csv",
    index=False
)


# ------------------
# PRODUCTS
# ------------------

products = pd.read_excel(
    DATA / "products.xlsx"
)

products = clean_strings(products)

products["price"] = (
    products["price"]
    .astype(str)
    .str.replace(",", ".")
)

products["price"] = pd.to_numeric(
    products["price"],
    errors="coerce"
)

products["is_active"] = (
    products["is_active"]
    .replace({
        "ИСТИНА": True,
        "ЛОЖЬ": False
    })
)

bad_prices = products["price"].isna()

for _, row in products[bad_prices].iterrows():
    save_problem(
        "products",
        row.to_dict(),
        "invalid price"
    )

products.to_csv(
    OUT / "products.csv",
    index=False
)


# ------------------
# LOG
# ------------------

with open(
    OUT / "problems.txt",
    "w",
    encoding="utf-8"
) as f:
    for line in log:
        f.write(line + "\n")

print("Done")