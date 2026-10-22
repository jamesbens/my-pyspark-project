from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, explode, split
from datetime import datetime

now = datetime.now()
formatted_string = now.strftime("%Y-%m-%d %H:%M:%S")
appname = "S3_corpus"
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
path = "s3a://my-pyspark-project-bckt/corpus.txt"
# spark.read.text reads the file into a single DataFrame column named 'value'
df = spark.read.text(path)

# 3. Explode words and calculate word counts
counts = (
    df.select(explode(split(col("value"), r"\s+")).alias("word"))
    .where(col("word") != "")  # Filter out empty strings caused by extra spaces
    .groupBy("word")
    .agg(count("*").alias("count"))
    .orderBy(col("count").desc())
)

# 4. Display top 20 words
counts.show(20)