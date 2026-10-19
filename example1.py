# Dataframe API is runninng on Pyspark SQL
from pyspark.sql import SparkSession, Row

spark = SparkSession.builder.getOrCreate()

df = spark.createDataFrame([
    Row(name='Alice', age = 25, weight = 71, height=171, employed=True),
    Row(name='Bob', age = 45, weight = 90, height=178, employed=True ),
    Row(name='Charles', age=37, weight=68, height=182, employed=False),
    Row(name='Daniel', age=52, weight=105, height=174, employed=True),
    Row(name='Eitan', age=24, weight=78, height=188, employed=True)
])
# query names of people older than 35
results = df.select('name').filter(df.age>35)
results.show()
df.show() # action
