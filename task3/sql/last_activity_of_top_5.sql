WITH top_customers AS (

    SELECT
        lco.hk_customer,
        COUNT(*) AS orders_count

    FROM sor.link_customer_order lco

    GROUP BY lco.hk_customer

    ORDER BY orders_count DESC

    LIMIT 5
)

SELECT
    hc.customer_id,
    sc.full_name,

    MAX(se.event_timestamp) AS last_activity,

    tc.orders_count

FROM top_customers tc

JOIN sor.hub_customer hc
    ON tc.hk_customer = hc.hk_customer

JOIN sor.sat_customer sc
    ON hc.hk_customer = sc.hk_customer

JOIN sor.link_customer_event lce
    ON hc.hk_customer = lce.hk_customer

JOIN sor.sat_event se
    ON lce.hk_event = se.hk_event

GROUP BY
    hc.customer_id,
    sc.full_name,
    tc.orders_count

ORDER BY tc.orders_count DESC;