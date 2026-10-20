from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, udf
from pyspark.sql.types import StringType


# Define UDF with return type
@udf(returnType=StringType())
def age_group(age):
    if age is None:
        return None
    if age < 30:
        return 'young'
    elif age < 60:
        return 'middle-aged'
    else:
        return 'senior'


# 1. Initialize SparkSession
spark = (
    SparkSession.builder
    .appName("S3_People_1000")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config(
        "spark.hadoop.fs.s3a.aws.credentials.provider",
        "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
    )
    .getOrCreate()
)

# 2. Read dataset from S3
path = "s3a://my-pyspark-project-bckt/people_1000.csv"
df = spark.read.csv(path, inferSchema=True, header=True)

# 3. Calculate BMI and Age Group
df_transformed = (
    df.withColumn('bmi', col('weight') / (col('height') / 100) ** 2)
      .withColumn('age_group', age_group(col('age')))
)

# 4. Aggregate by age_group
result = (
    df_transformed
      .groupBy('age_group')
      .agg(avg('bmi').alias('bmi_avg'))
)

#result.show()
result.coalesce(1).write.mode('overwrite').parquet('s3a://my-pyspark-project-bckt/example2_output')
