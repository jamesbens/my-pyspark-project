# Streaming - we keep receiving new information to be processed
# Execute the streamer.py before executing this script

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, explode, split
from datetime import datetime

now = datetime.now()
formatted_string = now.strftime("%Y-%m-%d %H:%M:%S")
appname = "streaming_app"
appname_dtm = f"{appname}_{formatted_string}"

# 1. Initialize SparkSession with S3 credentials
spark = (
    SparkSession.builder.appName(appname_dtm)
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.hadoop.fs.s3a.aws.credentials.provider",
            "software.amazon.awssdk.auth.credentials.EnvironmentVariableCredentialsProvider")
    .config("spark.hadoop.fs.s3a.connection.timeout", "60000")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# 2. Define the stream (Added .load() at the end)
lines = (
    spark.readStream
    .format('socket')
    .option('host', 'host.docker.internal') # or the IP where nc is running
    .option('port', 9999)
    .load()
)

# 3. Word count transformations (Fixed groupBy syntax)
words = lines.select(explode(split(col('value'), r'\s+')).alias('word'))
word_counts = words.groupBy('word').count()  # <-- FIX 2: Fixed groupBY to groupBy

# 4. Start the streaming query output to console
query = (
    word_counts.writeStream
    .outputMode("complete")  # "complete" mode allows aggregation results to display
    .format("console")
    .start()
)

query.awaitTermination()