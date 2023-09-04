-- currency_dim
INSERT INTO currency_dim (currency)
SELECT DISTINCT currency FROM raw_products;

-- category_dim
INSERT INTO category_dim (category)
SELECT DISTINCT category FROM raw_products;

-- type_dim
INSERT INTO type_dim (type)
SELECT DISTINCT type FROM raw_products;

-- Insert data in products_dim with related dimension IDs
INSERT INTO products_dim (uid, title, subtitle, category_id, type_id, currency_id, currentprice, rating)
SELECT
    rp.UID,
    rp.title,
    rp.subtitle,
    cd.ID AS category_id,
    td.ID AS type_id,
    curd.ID AS currency_id,
    rp.currentPrice,
    rp.rating
FROM raw_products rp
JOIN category_dim cd ON rp.category = cd.category
JOIN type_dim td ON rp.type = td.type
JOIN currency_dim curd ON rp.currency = curd.currency;


-- Insert data in sales_fact with related currency IDs and dimensions
INSERT INTO sales_fact (ticket_id, UID, currency_id, sales, quantity, ticket_date)
SELECT
    rs.ticket_id,
    rs.UID,
    curd.ID AS currency_id,
    rs.sales,
    rs.quantity,
    rs.ticket_date
FROM raw_sales rs
JOIN currency_dim curd ON rs.currency = curd.currency;
