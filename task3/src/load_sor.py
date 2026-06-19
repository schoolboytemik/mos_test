from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5432/mos"
)

queries = [

# ==========================
# HUBS
# ==========================

"""
INSERT INTO sor.hub_customer
SELECT DISTINCT
    decode(md5(customer_id::text), 'hex'),
    customer_id,
    CURRENT_TIMESTAMP,
    'raw.customers'
FROM raw.customers
ON CONFLICT (customer_id)
DO NOTHING;
""",

"""
INSERT INTO sor.hub_product
SELECT DISTINCT
    decode(md5(product_id::text), 'hex'),
    product_id,
    CURRENT_TIMESTAMP,
    'raw.products'
FROM raw.products
ON CONFLICT (product_id)
DO NOTHING;
""",

"""
INSERT INTO sor.hub_order
SELECT DISTINCT
    decode(md5(order_id::text), 'hex'),
    order_id,
    CURRENT_TIMESTAMP,
    'raw.orders'
FROM raw.orders
ON CONFLICT (order_id)
DO NOTHING;
""",

"""
INSERT INTO sor.hub_payment
SELECT DISTINCT
    decode(md5(payment_id::text), 'hex'),
    payment_id,
    CURRENT_TIMESTAMP,
    'raw.payments'
FROM raw.payments
ON CONFLICT (payment_id)
DO NOTHING;
""",

"""
INSERT INTO sor.hub_event
SELECT DISTINCT
    decode(md5(event_id::text), 'hex'),
    event_id,
    CURRENT_TIMESTAMP,
    'raw.events'
FROM raw.events
WHERE event_id IS NOT NULL
ON CONFLICT (event_id)
DO NOTHING;
""",

# ==========================
# SAT CUSTOMER
# ==========================

"""
INSERT INTO sor.sat_customer
SELECT
    decode(md5(customer_id::text), 'hex'),
    full_name,
    email,
    phone,
    city,
    created_at,

    decode(
        md5(
            concat_ws('|',
                full_name,
                email,
                phone,
                city,
                created_at
            )
        ),
        'hex'
    ),

    CURRENT_TIMESTAMP,
    'raw.customers'

FROM raw.customers

ON CONFLICT (hk_customer, hashdiff)
DO NOTHING;
""",

# ==========================
# SAT PRODUCT
# ==========================

"""
INSERT INTO sor.sat_product
SELECT
    decode(md5(product_id::text), 'hex'),
    product_name,
    category,
    price,
    currency,
    is_active,

    decode(
        md5(
            concat_ws('|',
                product_name,
                category,
                price,
                currency,
                is_active
            )
        ),
        'hex'
    ),

    CURRENT_TIMESTAMP,
    'raw.products'

FROM raw.products

ON CONFLICT (hk_product, hashdiff)
DO NOTHING;
""",

# ==========================
# SAT ORDER
# ==========================

"""
INSERT INTO sor.sat_order
SELECT
    decode(md5(order_id::text), 'hex'),
    quantity,
    unit_price,
    currency,
    order_timestamp,
    status,

    decode(
        md5(
            concat_ws('|',
                quantity,
                unit_price,
                currency,
                order_timestamp,
                status
            )
        ),
        'hex'
    ),

    CURRENT_TIMESTAMP,
    'raw.orders'

FROM raw.orders

ON CONFLICT (hk_order, hashdiff)
DO NOTHING;
""",

# ==========================
# SAT PAYMENT
# ==========================

"""
INSERT INTO sor.sat_payment
SELECT
    decode(md5(payment_id::text), 'hex'),
    payment_method,
    amount,
    currency,
    payment_timestamp,

    decode(
        md5(
            concat_ws('|',
                payment_method,
                amount,
                currency,
                payment_timestamp
            )
        ),
        'hex'
    ),

    CURRENT_TIMESTAMP,
    'raw.payments'

FROM raw.payments

ON CONFLICT (hk_payment, hashdiff)
DO NOTHING;
""",

# ==========================
# SAT EVENT
# ==========================

"""
INSERT INTO sor.sat_event
SELECT
    decode(md5(event_id::text), 'hex'),
    event_type,
    event_timestamp,

    decode(
        md5(
            concat_ws('|',
                event_type,
                event_timestamp
            )
        ),
        'hex'
    ),

    CURRENT_TIMESTAMP,
    'raw.events'

FROM raw.events
WHERE event_id IS NOT NULL

ON CONFLICT (hk_event, hashdiff)
DO NOTHING;
""",

# ==========================
# LINK CUSTOMER ORDER
# ==========================

"""
INSERT INTO sor.link_customer_order
SELECT DISTINCT
    decode(
        md5(
            customer_id::text || '|' || order_id::text
        ),
        'hex'
    ),

    decode(md5(customer_id::text), 'hex'),
    decode(md5(order_id::text), 'hex'),

    CURRENT_TIMESTAMP,
    'raw.orders'

FROM raw.orders

WHERE customer_id IS NOT NULL
  AND order_id IS NOT NULL

ON CONFLICT (hk_customer, hk_order)
DO NOTHING;
""",

# ==========================
# LINK ORDER PRODUCT
# ==========================

"""
INSERT INTO sor.link_order_product
SELECT DISTINCT
    decode(
        md5(
            order_id::text || '|' || product_id::text
        ),
        'hex'
    ),

    decode(md5(order_id::text), 'hex'),
    decode(md5(product_id::text), 'hex'),

    CURRENT_TIMESTAMP,
    'raw.orders'

FROM raw.orders

WHERE order_id IS NOT NULL
  AND product_id IS NOT NULL

ON CONFLICT (hk_order, hk_product)
DO NOTHING;
""",

# ==========================
# LINK ORDER PAYMENT
# ==========================

"""
INSERT INTO sor.link_order_payment
SELECT DISTINCT
    decode(
        md5(
            order_id::text || '|' || payment_id::text
        ),
        'hex'
    ),

    decode(md5(order_id::text), 'hex'),
    decode(md5(payment_id::text), 'hex'),

    CURRENT_TIMESTAMP,
    'raw.payments'

FROM raw.payments

WHERE order_id IS NOT NULL
  AND payment_id IS NOT NULL

ON CONFLICT (hk_order, hk_payment)
DO NOTHING;
""",

# ==========================
# LINK CUSTOMER EVENT
# ==========================

"""
INSERT INTO sor.link_customer_event
SELECT DISTINCT
    decode(
        md5(
            customer_id::text || '|' || event_id::text
        ),
        'hex'
    ),

    decode(md5(customer_id::text), 'hex'),
    decode(md5(event_id::text), 'hex'),

    CURRENT_TIMESTAMP,
    'raw.events'

FROM raw.events

WHERE customer_id IS NOT NULL
  AND event_id IS NOT NULL

ON CONFLICT (hk_customer, hk_event)
DO NOTHING;
""",

# ==========================
# LINK EVENT PRODUCT
# ==========================

"""
INSERT INTO sor.link_event_product
SELECT DISTINCT
    decode(
        md5(
            event_id::text || '|' || product_id::text
        ),
        'hex'
    ),

    decode(md5(event_id::text), 'hex'),
    decode(md5(product_id::text), 'hex'),

    CURRENT_TIMESTAMP,
    'raw.events'

FROM raw.events

WHERE event_id IS NOT NULL
  AND product_id IS NOT NULL

ON CONFLICT (hk_event, hk_product)
DO NOTHING;
"""
]

with engine.begin() as conn:

    for query in queries:
        conn.execute(text(query))

print("Done")