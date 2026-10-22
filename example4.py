# Same as exampl3 but
# Working directly with RDDs
from pyspark.sql import SparkSession
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
counts = (
    spark.sparkContext.textFile(path)
    .flatMap(lambda x: x.split())
    .map(lambda word: (word,1))
    .reduceByKey(lambda a, b: a + b)
)
print(counts.takeOrdered(20, key = lambda x: -x[1]))