from pyspark.sql import SparkSession
from datetime import datetime

now = datetime.now()
formatted_string = now.strftime("%Y-%m-%d %H:%M:%S")
appname = "customer_orders_RDD"
appname_dtm = f"{appname}_{formatted_string}"

# 1. Initialize SparkSession
spark = (
    SparkSession.builder.appName(appname_dtm)
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.hadoop.fs.s3a.aws.credentials.provider",
            "software.amazon.awssdk.auth.credentials.EnvironmentVariableCredentialsProvider")
    .config("spark.hadoop.fs.s3a.connection.timeout", "60000")
    .getOrCreate()
)

sc = spark.sparkContext

# Correct paths
orders_path = "s3a://my-pyspark-project-bckt/orders.csv"
customers_path = "s3a://my-pyspark-project-bckt/customers.csv"

# 2. Helper function to safely filter out header lines
def filter_header(line):
    # Skips common header keywords or empty rows
    return line and not line.startswith("order_id") and not line.startswith("customer_id")

# 3. Process Orders RDD -> (customer_id, amount)
# CSV schema assumption: order_id, customer_id, amount
orders_rdd = (
    sc.textFile(orders_path)
    .filter(filter_header)
    .map(lambda line: line.split(","))
    .map(lambda cols: (int(cols[1]), float(cols[2])))  # Key: customer_id (int), Value: amount (float)
)

# 4. Process Customers RDD -> (customer_id, country)
# CSV schema assumption: customer_id, name, country
customers_rdd = (
    sc.textFile(customers_path)
    .filter(filter_header)
    .map(lambda line: line.split(","))
    .map(lambda cols: (int(cols[0]), cols[2].strip()))  # Key: customer_id (int), Value: country (str)
)

# 5. Join and Aggregate
# Join yields: (customer_id, (amount, country))
result_rdd = (
    orders_rdd.join(customers_rdd)
    .map(lambda x: (x[1][1], (x[1][0], 1)))             # Map to: (country, (amount, count=1))
    .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))# Sum amounts and counts per country
    .mapValues(lambda x: x[0] / x[1])                   # Calculate average: sum / count
)

# 6. Collect and Display (Sorted descending by average amount)
sorted_results = sorted(result_rdd.collect(), key=lambda x: -x[1])

print(f"{'Country':<15} | {'Avg Amount':<10}")
print("-" * 28)
for country, avg_amount in sorted_results:
    print(f"{country:<15} | {avg_amount:<10.2f}")