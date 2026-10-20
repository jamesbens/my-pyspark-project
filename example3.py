# We will demonstrate the difference between the Dataframe API (high level) which is intuitive vs. working directly with the RDDs (Resilient Distributed Datasets - low level)
# We are going to count the words in a distributed way

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, split, explode
from pyspark.sql.types import StringType


# 1. Initialize SparkSession
spark = (
    SparkSession.builder
    .appName("S3_corpus")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config(
        "spark.hadoop.fs.s3a.aws.credentials.provider",
        "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
    )
    .getOrCreate()
)

# 2. Read dataset from S3
path = "s3a://my-pyspark-project-bckt/corpus.txt"
#split on every empty space or new row - this gonna be a word
# but we want the count of words on each row, hence we use explode
counts=(
         spark.read.txt(path, inferSchema=True, header=True)
        .select(explode(split(col('value'),r'\s+')).alias('word'))
        .groupBy(col('word').count())
        )
counts.orderBy(col('count').desc()).show(20)