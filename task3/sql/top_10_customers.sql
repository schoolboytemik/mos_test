SELECT
    c.customer_id,
    sc.full_name,
    SUM(sp.amount) AS total_amount

FROM sor.hub_customer c

JOIN sor.link_customer_order lco
    ON c.hk_customer = lco.hk_customer

JOIN sor.link_order_payment lop
    ON lco.hk_order = lop.hk_order

JOIN sor.sat_payment sp
    ON lop.hk_payment = sp.hk_payment

JOIN sor.sat_customer sc
    ON c.hk_customer = sc.hk_customer

WHERE sp.amount IS NOT NULL

GROUP BY
    c.customer_id,
    sc.full_name

ORDER BY total_amount DESC

LIMIT 10;