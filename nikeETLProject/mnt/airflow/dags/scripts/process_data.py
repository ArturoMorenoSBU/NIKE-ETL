import findspark
findspark.init()
from pyspark.sql import SparkSession
import subprocess
from os.path import abspath
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DecimalType, DateType
from pyspark.sql.functions import col

# Initialize Spark session
warehouse_location = abspath('spark-warehouse')
spark = SparkSession.builder \
    .appName("NikeDataProcessing") \
    .config("spark.sql.warehouse.dir", warehouse_location) \
    .enableHiveSupport() \
    .getOrCreate()

# Paths for CSV files
products_path = "hdfs://namenode:9000/raw_nike/data/products"
sales_base_path = "hdfs://namenode:9000/raw_nike/data/sales"

# Load products data and create Hive table "products"
products_df = spark.read.option("header", "true").csv(products_path)
#products_df.show()
products_columns = [
    "uid", "title", "subtitle", "category", "type", "currency",
    "fullPrice", "currentPrice", "rating", "prod_url", "color-Image-url"
]
products_df = products_df.select(*products_columns)
products_df.write.mode("overwrite").saveAsTable("products")


# Use Hadoop's hdfs command to list the directories in the sales_base_path
hdfs_list_cmd = ["hadoop", "fs", "-ls", sales_base_path]
hdfs_list_output = subprocess.check_output(hdfs_list_cmd).decode("utf-8")

# Parse the output to get the list of year directories
year_directories = [line.split()[-1] for line in hdfs_list_output.split("\n") if line]

# Process sales data for each year directory
for year_path in year_directories:
    if year_path.startswith("hdfs://"):
        # Use Hadoop's hdfs command to list the month directories within the year directory
        hdfs_list_cmd = ["hadoop", "fs", "-ls", year_path]
        hdfs_list_output = subprocess.check_output(hdfs_list_cmd).decode("utf-8")
        month_directories = [line.split()[-1] for line in hdfs_list_output.split("\n") if line]

        # Process sales data for each month directory within the year directory
        for month_path in month_directories:
            if month_path.startswith("hdfs://"):
                # Use Hadoop's hdfs command to list the day directories within the month directory
                hdfs_list_cmd = ["hadoop", "fs", "-ls", month_path]
                hdfs_list_output = subprocess.check_output(hdfs_list_cmd).decode("utf-8")
                day_directories = [line.split()[-1] for line in hdfs_list_output.split("\n") if line]

                # Process sales data for each day directory within the month directory
                for day_path in day_directories:
                    if day_path.startswith("hdfs://") and ".DS_Store" not in day_path:
                        
                        # Define the schema for the sales data
                        sales_schema = StructType([
                            StructField("_c0", IntegerType(), False),
                            StructField("_c1", IntegerType(), False),
                            StructField("_c2", StringType(), False),
                            StructField("_c3", StringType(), False),
                            StructField("_c4", DecimalType(10, 2), False),
                            StructField("_c5", IntegerType(), False),
                            StructField("_c6", DateType(), False)
                        ])
                        print(f'This is the day_path {day_path}')


                        # Read the sales data with the specified schema
                        sales_df = spark.read.option("header", "false").csv(day_path)
                        
                        sales_df = sales_df.select(
                            "_c0","_c1", "_c2", "_c3", "_c4", "_c5", "_c6"
                        )
                        sales_df.show()
                        #break
                        # Append the current day's sales data to the combined_sales_df DataFrame
                        if 'combined_sales_df' in locals():
                            combined_sales_df = combined_sales_df.union(sales_df)
                        else:
                            combined_sales_df = sales_df
                        
                        # Get the second row as the new header
                        new_header = ["_c0","ticket_id","UID","currency","sales","quantity", "ticket_date"]
                        

                        # Convert the Row object to a list of column names
                        new_column_names = new_header

                        # Rename the columns using the new header
                        for i, column_name in enumerate(new_column_names):
                            combined_sales_df = combined_sales_df.withColumnRenamed(combined_sales_df.columns[i], column_name)

                        # Drop the first row (old header)
                        combined_sales_df = combined_sales_df.filter(col(combined_sales_df.columns[0]) != "null")


# Write the combined sales data DataFrame to the Hive table "sales"
combined_sales_df.write.mode("overwrite").saveAsTable("sales")


# Stop the Spark session
spark.stop()
