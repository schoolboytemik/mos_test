CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.customers  (
    customer_id     BIGINT,
    full_name       TEXT,
    email           TEXT,
    phone           TEXT,
    city            TEXT,
    created_at      TIMESTAMP,

    load_dttm       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_file     TEXT
);

CREATE TABLE IF NOT EXISTS raw.events  (
    event_id         BIGINT,
    customer_id      BIGINT,
    event_type       TEXT,
    event_timestamp  TIMESTAMP,
    product_id       BIGINT,

    load_dttm        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_file      TEXT
);

CREATE TABLE IF NOT EXISTS raw.orders  (
    order_id         BIGINT,
    customer_id      BIGINT,
    product_id       BIGINT,
    quantity         INTEGER,
    unit_price       NUMERIC(12,2),
    currency         VARCHAR(3),
    order_timestamp  TIMESTAMP,
    status           TEXT,

    load_dttm        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_file      TEXT
);

CREATE TABLE IF NOT EXISTS raw.payments  (
    payment_id         BIGINT,
    order_id           BIGINT,
    payment_method     TEXT,
    amount             NUMERIC(12,2),
    currency           VARCHAR(3),
    payment_timestamp  TIMESTAMP,

    load_dttm          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_file        TEXT
);

CREATE TABLE IF NOT EXISTS raw.products (
    product_id      BIGINT,
    product_name    TEXT,
    category        TEXT,
    price           NUMERIC(12,2),
    currency        VARCHAR(3),
    is_active       BOOLEAN,

    load_dttm       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_file     TEXT
);