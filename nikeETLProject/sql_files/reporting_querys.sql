--Query the top 5 sales by product
SELECT
    p.title,
    p.subtitle,
    SUM(sf.sales) AS total_sales
FROM products_dim p
JOIN sales_fact sf ON p.UID = sf.UID
GROUP BY p.title, p.subtitle
ORDER BY total_sales DESC
LIMIT 5;

-- Query the top 5 sales by category agrupation
SELECT
    c.category,
    SUM(sf.sales) AS total_sales
FROM category_dim c
JOIN products_dim p ON c.ID = p.category_id
JOIN sales_fact sf ON p.UID = sf.UID
GROUP BY c.category
ORDER BY total_sales DESC
LIMIT 5;

--least 5 sales by category
SELECT
    c.category,
    SUM(sf.sales) AS total_sales
FROM category_dim c
JOIN products_dim p ON c.ID = p.category_id
JOIN sales_fact sf ON p.UID = sf.UID
GROUP BY c.category
ORDER BY total_sales ASC
LIMIT 5;
--top 5 sales by title and subtitle
SELECT
    p.title,
    p.subtitle,
    SUM(sf.sales) AS total_sales
FROM products_dim p
JOIN sales_fact sf ON p.UID = sf.UID
GROUP BY p.title, p.subtitle
ORDER BY total_sales DESC
LIMIT 5;

-- top 3 products that has the greatest sales by category

WITH ranked_products AS (
    SELECT
        p.title,
        p.subtitle,
        c.category,
        SUM(sf.sales) AS total_sales,
        ROW_NUMBER() OVER (PARTITION BY c.category ORDER BY SUM(sf.sales) DESC) AS rn
    FROM products_dim p
    JOIN category_dim c ON p.category_id = c.ID
    JOIN sales_fact sf ON p.UID = sf.UID
    GROUP BY p.title, p.subtitle, c.category
)
SELECT
    title,
    subtitle,
    category,
    total_sales
FROM ranked_products
WHERE rn <= 3;