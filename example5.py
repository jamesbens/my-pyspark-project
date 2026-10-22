# Joining DataFrames

from pyspark.sql import SparkSession
from datetime import datetime
from pyspark.sql.functions import col, count, explode, split

now = datetime.now()
formatted_string = now.strftime("%Y-%m-%d %H:%M:%S")
appname = "customer_orders"
appname_dtm = f"{appname}_{formatted_string}"

# 1. Initialize SparkSession with S3 credentials
spark = (
    SparkSession.builder.appName(appname_dtm)
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.hadoop.fs.s3a.aws.credentials.provider",
            "software.amazon.awssdk.auth.credentials.EnvironmentVariableCredentialsProvider")
    # CORRECT (Specify integer in milliseconds):
    .config("spark.hadoop.fs.s3a.connection.timeout", "60000")
    .getOrCreate()
)

# 2. Read plain text dataset from S3
orders_path = "s3a://my-pyspark-project-bckt/customers.csv"
customers_path = "s3a://my-pyspark-project-bckt/orders.csv"

# create the dataframes
orders=spark.read.csv(orders_path, header=True, inferSchema=True)
customers=spark.read.csv(customers_path, header=True, inferSchema=True)

result_df= (
    orders.join(customers, 'customer_id')
    .groupBy("country")
    .avg('amount')
    .orderBy(col("avg(amount)").desc())
)

# Display results
result_df.show()

# 4. Save results back to S3
output_path = "s3a://my-pyspark-project-bckt/output/avg_amount_by_country"
#result_df.orderBy(col('avg(amount)').desc()).show()
result_df.write.mode("overwrite").format("csv").option("header", "true").save(output_path)