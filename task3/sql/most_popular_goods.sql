SELECT
    hp.product_id,
    sp.product_name,

    COUNT(*) AS orders_count

FROM sor.link_order_product lop

JOIN sor.hub_product hp
    ON lop.hk_product = hp.hk_product

JOIN sor.sat_product sp
    ON hp.hk_product = sp.hk_product

GROUP BY
    hp.product_id,
    sp.product_name

ORDER BY orders_count DESC;