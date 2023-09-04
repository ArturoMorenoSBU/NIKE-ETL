CREATE OR REPLACE TABLE currency_dim (
    ID INT PRIMARY KEY AUTOINCREMENT START 1 INCREMENT 1
    , currency TEXT
);


CREATE OR REPLACE TABLE category_dim (
    ID INT PRIMARY KEY AUTOINCREMENT START 1 INCREMENT 1
    , category TEXT
);

CREATE OR REPLACE TABLE type_dim (
    ID INT PRIMARY KEY AUTOINCREMENT START 1 INCREMENT 1
    , type TEXT
);

CREATE OR REPLACE TABLE products_dim (
    uid TEXT,
    title TEXT,
    subtitle TEXT,
    category_id INT,
    type_id INT,
    currency_id INT,
    currentprice NUMBER(6, 2),
    rating NUMBER(3, 1),
    FOREIGN KEY (category_id) REFERENCES category_dim(ID),
    FOREIGN KEY (type_id) REFERENCES type_dim(ID),
    FOREIGN KEY (currency_id) REFERENCES currency_dim(ID)
);
CREATE OR REPLACE TABLE sales_fact (
    ticket_id INTEGER,
    UID TEXT,
    currency_id INTEGER,
    sales NUMERIC(6,2),
    quantity INTEGER,
    ticket_date DATE,
    FOREIGN KEY (currency_id) REFERENCES currency_dim(ID)
);
