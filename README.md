# my-pyspark-project
demonstrates how to utilize Docker Compose to simulate a cluster with one master and four worker nodes.
This practical guide covers essential concepts like Resilient Distributed Datasets, lazy evaluation, and shuffle operations, 
while also showcasing how to build ETL pipelines that process large-scale datasets stored in AWS S3 buckets.

Step1
creating master-workers infra on dockers and manipulating distributed data with PySpark

Step2
distributing large data (1 GB) in AWS S3 buckets.
Then define the workers to handle this data.
At the end we will aggregate everything again into one S3 bucket in a partition
Goto AWS Console -> S3 -> Create Bucket -> name if my-pyspark-project-bckt

Create a user entitled to access this bucket.
Goto IAM -> IAM users -> Create user-> name it: pyspark_user
-> next -> Attach policies directly -> Search S3FullAccess and select -> Next -> Create User

Goto the pyspark_user -> Click on Create Access Key -> Select CLI and accept conditions
-> Next - set description -> Copy access Key

Then we create a file called .env
Then there are 2 key values we want to create:
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS

Generate with AI a 1.5 GB people.csv file dataset has been generated with synthetic records 
containing realistic values for each specified column (name, age, weight, height, employed).

Upload the file to S3.
Create file example2.py.
specify the path of the people.csv in S3.

