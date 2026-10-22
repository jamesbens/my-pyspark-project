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

orders_path = "s3a://my-pyspark-project-bckt/orders.csv"
customers_path = "s3a://my-pyspark-project-bckt/customers.csv"

# Helper function to split CSV lines safely
def parse_csv(line):
    return [col.strip(' "\'\t\r\n') for col in line.split(",")]

# 2. Process Orders RDD -> (customer_id: str, amount: float)
orders_rdd = (
    sc.textFile(orders_path)
    .map(parse_csv)
    .filter(lambda cols: len(cols) >= 3 and cols[1] != "customer_id") # Filter out header and invalid rows
    .map(lambda cols: (str(cols[1]), float(cols[2])))                 # Keep customer_id as string
)

# 3. Process Customers RDD -> (customer_id: str, country: str)
customers_rdd = (
    sc.textFile(customers_path)
    .map(parse_csv)
    .filter(lambda cols: len(cols) >= 3 and cols[0] != "customer_id") # Filter out header and invalid rows
    .map(lambda cols: (str(cols[0]), cols[2]))                         # Keep customer_id as string
)

# 4. Join and Aggregate
# Join yields: (customer_id, (amount, country))
result_rdd = (
    orders_rdd.join(customers_rdd)
    .map(lambda x: (x[1][1], (x[1][0], 1)))              # Map to: (country, (amount, count=1))
    .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1])) # Sum amounts and counts per country
    .mapValues(lambda x: x[0] / x[1])                    # Calculate average: sum / count
)

# 5. Collect and Display
sorted_results = sorted(result_rdd.collect(), key=lambda x: -x[1])

print(f"{'Country':<15} | {'Avg Amount':<10}")
print("-" * 28)
for country, avg_amount in sorted_results:
    print(f"{country:<15} | {avg_amount:<10.2f}")