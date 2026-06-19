CREATE SCHEMA IF NOT EXISTS sor;

CREATE TABLE sor.hub_customer (
    hk_customer     BYTEA PRIMARY KEY,
    customer_id     BIGINT NOT NULL UNIQUE,

    load_dttm       TIMESTAMP NOT NULL,
    record_source   TEXT NOT NULL
);

CREATE TABLE sor.hub_product (
    hk_product      BYTEA PRIMARY KEY,
    product_id      BIGINT NOT NULL UNIQUE,

    load_dttm       TIMESTAMP NOT NULL,
    record_source   TEXT NOT NULL
);

CREATE TABLE sor.hub_order (
    hk_order        BYTEA PRIMARY KEY,
    order_id        BIGINT NOT NULL UNIQUE,

    load_dttm       TIMESTAMP NOT NULL,
    record_source   TEXT NOT NULL
);

CREATE TABLE sor.hub_payment (
    hk_payment      BYTEA PRIMARY KEY,
    payment_id      BIGINT NOT NULL UNIQUE,

    load_dttm       TIMESTAMP NOT NULL,
    record_source   TEXT NOT NULL
);

CREATE TABLE sor.hub_event (
    hk_event        BYTEA PRIMARY KEY,
    event_id        BIGINT NOT NULL UNIQUE,

    load_dttm       TIMESTAMP NOT NULL,
    record_source   TEXT NOT NULL
);

CREATE TABLE sor.sat_customer (
    hk_customer     BYTEA NOT NULL,

    full_name       TEXT,
    email           TEXT,
    phone           TEXT,
    city            TEXT,
    created_at      TIMESTAMP,

    hashdiff        BYTEA NOT NULL,

    load_dttm       TIMESTAMP NOT NULL,
    record_source   TEXT NOT NULL,
    UNIQUE (hk_customer, hashdiff)
);

CREATE TABLE sor.sat_product (
    hk_product      BYTEA NOT NULL,

    product_name    TEXT,
    category        TEXT,
    price           NUMERIC(12,2),
    currency        CHAR(3),
    is_active       BOOLEAN,

    hashdiff        BYTEA NOT NULL,

    load_dttm       TIMESTAMP NOT NULL,
    record_source   TEXT NOT NULL,
    UNIQUE (hk_product, hashdiff)
);

CREATE TABLE sor.sat_order (
    hk_order        BYTEA NOT NULL,

    quantity        INTEGER,
    unit_price      NUMERIC(12,2),
    currency        CHAR(3),
    order_timestamp TIMESTAMP,
    status          TEXT,

    hashdiff        BYTEA NOT NULL,

    load_dttm       TIMESTAMP NOT NULL,
    record_source   TEXT NOT NULL,
    UNIQUE (hk_order, hashdiff)
);

CREATE TABLE sor.sat_payment (
    hk_payment          BYTEA NOT NULL,

    payment_method      TEXT,
    amount              NUMERIC(12,2),
    currency            CHAR(3),
    payment_timestamp   TIMESTAMP,

    hashdiff            BYTEA NOT NULL,

    load_dttm           TIMESTAMP NOT NULL,
    record_source       TEXT NOT NULL,
    UNIQUE (hk_payment, hashdiff)
);

CREATE TABLE sor.sat_event (
    hk_event            BYTEA NOT NULL,

    event_type          TEXT,
    event_timestamp     TIMESTAMP,

    hashdiff            BYTEA NOT NULL,

    load_dttm           TIMESTAMP NOT NULL,
    record_source       TEXT NOT NULL,
    UNIQUE (hk_event, hashdiff)
);

CREATE TABLE sor.link_customer_order (
    hk_customer_order   BYTEA PRIMARY KEY,

    hk_customer         BYTEA NOT NULL,
    hk_order            BYTEA NOT NULL,

    load_dttm           TIMESTAMP NOT NULL,
    record_source       TEXT NOT NULL,
    UNIQUE (hk_customer, hk_order)
);

CREATE TABLE sor.link_order_product (
    hk_order_product    BYTEA PRIMARY KEY,

    hk_order            BYTEA NOT NULL,
    hk_product          BYTEA NOT NULL,

    load_dttm           TIMESTAMP NOT NULL,
    record_source       TEXT NOT NULL,
    UNIQUE (hk_order, hk_product)
);

CREATE TABLE sor.link_order_payment (
    hk_order_payment    BYTEA PRIMARY KEY,

    hk_order            BYTEA NOT NULL,
    hk_payment          BYTEA NOT NULL,

    load_dttm           TIMESTAMP NOT NULL,
    record_source       TEXT NOT NULL,
    UNIQUE (hk_order, hk_payment)
);

CREATE TABLE sor.link_customer_event (
    hk_customer_event   BYTEA PRIMARY KEY,

    hk_customer         BYTEA NOT NULL,
    hk_event            BYTEA NOT NULL,

    load_dttm           TIMESTAMP NOT NULL,
    record_source       TEXT NOT NULL,
    UNIQUE (hk_customer, hk_event)
);

CREATE TABLE sor.link_event_product (
    hk_event_product    BYTEA PRIMARY KEY,

    hk_event            BYTEA NOT NULL,
    hk_product          BYTEA NOT NULL,

    load_dttm           TIMESTAMP NOT NULL,
    record_source       TEXT NOT NULL,
    UNIQUE (hk_event, hk_product)
);