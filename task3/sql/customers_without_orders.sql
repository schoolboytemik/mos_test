SELECT
    hc.customer_id,
    sc.full_name

FROM sor.hub_customer hc

JOIN sor.sat_customer sc
    ON hc.hk_customer = sc.hk_customer

LEFT JOIN sor.link_customer_order lco
    ON hc.hk_customer = lco.hk_customer

WHERE lco.hk_customer IS NULL

ORDER BY hc.customer_id;