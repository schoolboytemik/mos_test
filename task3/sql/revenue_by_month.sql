SELECT
    DATE_TRUNC(
        'month',
        payment_timestamp
    ) AS month,

    SUM(amount) AS revenue

FROM sor.sat_payment

GROUP BY month

ORDER BY month;