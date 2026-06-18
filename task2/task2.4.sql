SELECT
    t1.id AS id1,
    t2.id AS id2,
    t1.category
FROM items t1
JOIN items t2
    ON t1.name = t2.name
   AND t1.category = t2.category
   AND t1.id < t2.id;