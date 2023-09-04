            CREATE EXTERNAL TABLE IF NOT EXISTS products(     
                UID              VARCHAR(100),
                title            VARCHAR(100),
                subtitle         VARCHAR(100),
                category         VARCHAR(100),
                type             VARCHAR(100),
                currency         VARCHAR(100),
                fullPrice        INTEGER ,
                currentPrice     NUMERIC(6,2),
                rating           NUMERIC(3,1),
                prod_url         VARCHAR(100),
                colorImageurl    VARCHAR(100)
            )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE;


            CREATE EXTERNAL TABLE IF NOT EXISTS sales(     
                c0_1    INTEGER,
                ticket_id INTEGER,
                UID       VARCHAR(100),
                currency  VARCHAR(3),
                sales     NUMERIC(6,2),
                quantity  INTEGER,
                ticket_date   DATE
            )
            
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE;