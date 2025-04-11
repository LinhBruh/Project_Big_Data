# test_spark.py
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("TestSpark").master("spark://spark-master/7077").getOrCreate()
print("🔥 Spark is working!")
spark.stop()
