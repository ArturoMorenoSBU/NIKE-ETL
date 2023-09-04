from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "algo@localhost.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

with DAG("nike_pipeline", start_date=datetime(2023, 8, 18), 
         schedule_interval="@daily", default_args=default_args, catchup=False) as dag:

    nike_scraper_task = BashOperator(
        task_id='getTheData_fromNike',
        bash_command='cd /opt/airflow/dags/scrapper/ && python main.py',

    )

    save_data = BashOperator(
        #Create a dir /nike_raw in hdfs and then move the files to that directory
        task_id = "SavingInHdfs",
        bash_command = """
            hdfs dfs -mkdir -p /raw_nike
            hdfs dfs -put -f $AIRFLOW_HOME/dags/scrapper/data /raw_nike
        """
    )

    creating_products_and_sales_tables = HiveOperator(
        task_id = "create_products_and_sales_tables",
        hive_cli_conn_id="hive_conn",
        hql="""
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


        """
    )


    processing_task = BashOperator(
    task_id="processing_the_data",
    bash_command='cd /opt/airflow/dags/scripts && python process_data.py',
    )



nike_scraper_task >> save_data >> creating_products_and_sales_tables >> processing_task
