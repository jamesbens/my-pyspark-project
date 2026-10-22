docker exec -it pyspark2-spark-master-1 /opt/spark/bin/spark-submit `
  --master spark://spark-master:7077 `
  --packages org.apache.hadoop:hadoop-aws:3.5.0,software.amazon.awssdk:bundle:2.35.4  `
  --conf spark.jars.ivy=/tmp/.ivy2 `
  --conf spark.network.timeout=800s `
  --conf spark.files.fetchTimeout=1200s `
  /opt/spark/work-dir/example4.py
