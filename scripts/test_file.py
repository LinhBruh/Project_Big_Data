from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MongoTest") \
    .master("spark://spark-master:7077") \
    .config("spark.jars", ",".join([
        "/opt/spark/jars/mongo-spark-connector_2.12-10.4.1.jar",
        "/opt/spark/jars/mongodb-driver-sync-4.11.1.jar",
        "/opt/spark/jars/mongodb-driver-core-4.11.1.jar",
        "/opt/spark/jars/bson-4.11.1.jar"
    ])) \
    .config("spark.mongodb.read.connection.uri", "mongodb://admin:password@mongodb:27017") \
    .config("spark.mongodb.read.database", "sales_db") \
    .getOrCreate()

df = spark.read.format("mongodb") \
    .option("spark.mongodb.read.collection", "customers") \
    .load()

print(df.head(5))
spark.stop()