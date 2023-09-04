# Hello world!
The scope I used for this project is a ETL pipeline.


## Quick resume
1. For this project I used Airflow as orchestrator.
2. I used Docker for the environment configurations.
3. The data was extracted from nike's website API  "https://www.nike.com".
4. Use of hdfs to store the raw data.
5. Use of hive to manage the data stored in hdfs.
6. Use of Spark to process the data.
7. Use of Hue as an open-source SQL Assistant for Databases & Data Warehouses, for the query and the report.


![1](https://github.com/ArturoMorenoSBU/NIKE-ETL/assets/34179305/986bc7ad-9d18-42a7-818e-31af85e7eafa)



## Docker-compose overview.

The docker compose have the definition of the services used for this project.
 * DATABASE SERVICE
 * HADOOP SERVICES
 * SPARK SERVICES
 * AIRFLOW
 * NETWORK

Every service has a dockerfile with extra details for the configuration in the directory /docker

## Running docker-compose and getting the containers!

Run the containers with the following command.

    docker-compose up -d

### Right!, the containers are up now.
![2](https://github.com/ArturoMorenoSBU/NIKE-ETL/assets/34179305/c0719b86-fdf6-43f8-8cef-dba493be6597)



## The orchestrator

Into the directory **/mnt/airflow/dags** is the nike_pipeline.py file that describes the pipeline of Nike's ETL workflow using the DAG approach.
This is an overall view of the dag.


## Let's take a look every task in the Nike DAG.
![3](https://github.com/ArturoMorenoSBU/NIKE-ETL/assets/34179305/9edeeab7-9f1a-4818-8aa7-be6cced4fc61)


The dag is in this directory: /mnt/airflow/dags/nike_pipeline.py

1. **getTheData_fromNike**: This task helps us to run the **file nikescrapi.py** that is into the **/mnt/airflow/dags/scrapper/**
   In this task, I used the BashOperator to run the scrap script.
![4](https://github.com/ArturoMorenoSBU/NIKE-ETL/assets/34179305/38d81b31-bd7f-4847-abbb-1d67739bef71)


   
2. **SavingInHdfs**: For this task we define the partitions into the hdsf, first I created a **/raw_nike** directory to put all the files with the following distribution:
   
    ![5](https://github.com/ArturoMorenoSBU/NIKE-ETL/assets/34179305/5f4b21e5-6c00-420e-b8f5-c6b3314f41da)



     To do that, the task was accomplished with a bash operator
   ![6](https://github.com/ArturoMorenoSBU/NIKE-ETL/assets/34179305/eecbd049-c52b-47f8-b7ee-01300065c075)


   ![7](https://github.com/ArturoMorenoSBU/NIKE-ETL/assets/34179305/f7908d80-3560-429c-a176-6d2eefd213b1)
   

3. **create_products_and_sales_tables**: Once the data is in the hdfs, I used the hiveOperator to define the sales and product tables, these files will be used to store the data that will be processed after. Is necessary to set the hive connection in airflow.
You can check the external tables definition in the directory sql_files/definition_processed_tables.sql
    ![8](https://github.com/ArturoMorenoSBU/NIKE-ETL/assets/34179305/29e22d91-9aab-421a-899c-15c33511bd64)

    ![9](https://github.com/ArturoMorenoSBU/NIKE-ETL/assets/34179305/c49b7ffa-de4f-411a-a7f4-f4684bad9255)



4. **processing_the_data**: Once the data is in hdfs and the external tables are defined using hive, is time to process the data.
   To do that, I used Apache Spark to process the data, you can find the whole code in /mnt/airflow/dags/scripts/process_data.py.
   ![10](https://github.com/ArturoMorenoSBU/NIKE-ETL/assets/34179305/ec91b46e-f893-42ab-a15d-e98ba9a803e0)



   ## HUE
   Hue is an open-source SQL Assistant for Databases and Data Warehouses, I used its web-user interface to create and fill the fact and dim tables for the 
   analysis

   Here we can query the information for the processed product and sales information.

   ![11](https://github.com/ArturoMorenoSBU/NIKE-ETL/assets/34179305/0cb969b3-7e56-4e10-8558-ec13be99cdba)


   ![12](https://github.com/ArturoMorenoSBU/NIKE-ETL/assets/34179305/be29082b-5f4d-4b53-afbc-b7c976df44ac)

   
## The fact and dimension table are configured as follows.
   ![13](https://github.com/ArturoMorenoSBU/NIKE-ETL/assets/34179305/82c2bfc7-fea9-4eeb-b725-24b9e656154b)


The SQL commands to create these tables are defined in **/sql_files/create_fact_dim_tables.sql**

The SQL commands to fulfill these tables with the processed data are on **/sql_files/fill_fact_and_dim_tables.sql**


Hue allows us to query the following requests:
    1. Query the top 5 sales by product
    2. Query the top 5 sales by category agrupation
    3. Query the least 5 sales by category agrupation
    4. Query the top 5 sales by title and subtitle agrupation
    5. Query the top 3 products that has the greatest sales by category

The reporting for the results of these queries are on **/report_results** and the queries to retrieve these results are on /sql_files/reporting_querys.sql
