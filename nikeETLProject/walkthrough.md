# Hello world!
This is the walkthrough of my project to Data-Engineering-101
The scope I used for this project is a ETL pipeline.


## Quick resume
1. For this project I used Airflow as orchestrator.
2. I used Docker for the environment configurations.
3. The data was extracted from nike's website API  "https://www.nike.com".
4. Use of hdfs to store the raw data.
5. Use of hive to manage the data stored in hdfs.
6. Use of Spark to process the data.
7. Use of Hue as an open-source SQL Assistant for Databases & Data Warehouses, for the query and the report.


![WhatsApp Image 2023-08-24 at 10 06 39 PM (1)](https://github.com/Data-Engineering-101/de-101-project-artusenroute/assets/105809768/ff674a43-0da7-4b49-bc4f-e5e239f5f3b2)


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
<img width="464" alt="Captura de pantalla 2023-08-23 a la(s) 21 07 54" src="https://github.com/Data-Engineering-101/de-101-project-artusenroute/assets/105809768/d0d13acb-bc27-4e3f-bc45-4d3e2f2049b9">


## The orchestrator

Into the directory **/mnt/airflow/dags** is the nike_pipeline.py file that describes the pipeline of Nike's ETL workflow using the DAG approach.
This is an overall view of the dag.


## Let's take a look every task in the Nike DAG.
![Captura de pantalla 2023-08-23 a la(s) 21 19 45](https://github.com/Data-Engineering-101/de-101-project-artusenroute/assets/105809768/263b5525-a852-40cf-8503-d558537347f9)

The dag is in this directory: /mnt/airflow/dags/nike_pipeline.py

1. **getTheData_fromNike**: This task helps us to run the **file nikescrapi.py** that is into the **/mnt/airflow/dags/scrapper/**
   In this task, I used the BashOperator to run the scrap script.
   ![Captura de pantalla 2023-08-23 a la(s) 21 54 31](https://github.com/Data-Engineering-101/de-101-project-artusenroute/assets/105809768/c555b63d-e441-4b4d-bb5a-bd34309bea80)

   
2. **SavingInHdfs**: For this task we define the partitions into the hdsf, first I created a **/raw_nike** directory to put all the files with the following distribution:
   
    ![Captura de pantalla 2023-08-23 a la(s) 21 47 35](https://github.com/Data-Engineering-101/de-101-project-artusenroute/assets/105809768/a8bdfa86-f4d6-4498-8d9d-14f93f7c8c89)


     To do that, the task was accomplished with a bash operator
   ![Captura de pantalla 2023-08-23 a la(s) 22 03 01](https://github.com/Data-Engineering-101/de-101-project-artusenroute/assets/105809768/99ae9752-de98-49d3-a711-66469f833cea)

 
    <img width="587" alt="Captura de pantalla 2023-08-23 a la(s) 21 29 43" src="https://github.com/Data-Engineering-101/de-101-project-artusenroute/assets/105809768/b38b9d9e-af44-4441-85e4-4fd9bf2b9e4c">

3. **create_products_and_sales_tables**: Once the data is in the hdfs, I used the hiveOperator to define the sales and product tables, these files will be used to store the data that will be processed after. Is necessary to set the hive connection in airflow.
You can check the external tables definition in the directory sql_files/definition_processed_tables.sql
    ![hive-coonn](https://github.com/Data-Engineering-101/de-101-project-artusenroute/assets/105809768/31e276ff-ea0f-4895-bd6e-766b6baccd20)
    ![Captura de pantalla 2023-08-23 a la(s) 22 09 09](https://github.com/Data-Engineering-101/de-101-project-artusenroute/assets/105809768/474f3b7f-dda0-4b40-97cc-870d1bbb6c99)


4. **processing_the_data**: Once the data is in hdfs and the external tables are defined using hive, is time to process the data.
   To do that, I used Apache Spark to process the data, you can find the whole code in /mnt/airflow/dags/scripts/process_data.py.
   ![Captura de pantalla 2023-08-23 a la(s) 22 09 16](https://github.com/Data-Engineering-101/de-101-project-artusenroute/assets/105809768/5a997809-1aac-4da2-88d2-d59c01b79601)


   ## HUE
   Hue is an open-source SQL Assistant for Databases and Data Warehouses, I used its web-user interface to create and fill the fact and dim tables for the 
   analysis

   Here we can query the information for the processed product and sales information.

   <img width="680" alt="Captura de pantalla 2023-08-24 a la(s) 00 30 09" src="https://github.com/Data-Engineering-101/de-101-project-artusenroute/assets/105809768/4638599c-71e7-41aa-94f1-f2ed41978ece">

   <img width="680" alt="Captura de pantalla 2023-08-24 a la(s) 00 30 25" src="https://github.com/Data-Engineering-101/de-101-project-artusenroute/assets/105809768/f7e336d8-e025-4cde-a185-2e5d3641983a">
   
## The fact and dimension table are configured as follows.
   ![Captura de pantalla 2023-08-24 a la(s) 00 52 11](https://github.com/Data-Engineering-101/de-101-project-artusenroute/assets/105809768/321574e1-8943-4e3d-bca4-9f0de9218b88)

The SQL commands to create these tables are defined in **/sql_files/create_fact_dim_tables.sql**

The SQL commands to fulfill these tables with the processed data are on **/sql_files/fill_fact_and_dim_tables.sql**


Hue allows us to query the following requests:
    1. Query the top 5 sales by product
    2. Query the top 5 sales by category agrupation
    3. Query the least 5 sales by category agrupation
    4. Query the top 5 sales by title and subtitle agrupation
    5. Query the top 3 products that has the greatest sales by category

The reporting for the results of these queries are on **/report_results** and the queries to retrieve these results are on /sql_files/reporting_querys.sql
