from pyspark.sql import SparkSession
from pyspark import StorageLevel
import json

spark = SparkSession.builder \
    .appName("MongoHDFS") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .config("spark.mongodb.read.connection.uri", "mongodb://admin:password@mongodb:27017") \
    .config("spark.mongodb.read.database", "sales_db") \
    .config("spark.sql.shuffle.partitions", "12") \
    .config("spark.default.parallelism", "12") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.memory", "3g") \
    .config("spark.executor.instances", "3") \
    .config("spark.executor.cores", "1") \
    .config("spark.network.timeout", "1000s") \
    .config("spark.executor.heartbeatInterval", "60s") \
    .config("spark.memory.fraction", "0.4") \
    .config("spark.memory.storageFraction", "0.1") \
    .config("spark.sql.parquet.compression.codec", "snappy") \
    .config("spark.jars", ",".join([
        "/opt/spark/jars/mongo-spark-connector_2.12-10.4.1.jar",
        "/opt/spark/jars/mongodb-driver-sync-4.11.1.jar",
        "/opt/spark/jars/mongodb-driver-core-4.11.1.jar",
        "/opt/spark/jars/bson-4.11.1.jar"
    ])) \
    .getOrCreate()


def extract_normal_collections():
    collections = ["customers", "products", "inventory"]
    for col in collections:
        print(f"Extracting: {col}")
        df = spark.read.format("mongodb") \
            .option("spark.mongodb.read.collection", col) \
            .load()

        df = df.persist(StorageLevel.DISK_ONLY)

        df.repartition(6).write.mode("overwrite") \
            .option("compression", "snappy") \
            .parquet(f"hdfs://namenode:9000/data/sales_db/{col}")

        print(f"Finished: {col}")


def extract_orders_by_year():
    for year in range(2017, 2026):
        start_date = f"{year}-01-01 00:00:00"
        end_date = f"{year + 1}-01-01 00:00:00"

        print(f"Extracting orders for year {year}")

        pipeline = json.dumps([
            {"$match": {
                "order_date": {
                    "$gte": {"$date": start_date},
                    "$lt": {"$date": end_date}
                }
            }}
        ])

        df = spark.read.format("mongodb") \
            .option("spark.mongodb.read.collection", "orders") \
            .option("pipeline", pipeline) \
            .option("spark.mongodb.input.partitioner", "MongoPaginateBySizePartitioner") \
            .option("spark.mongodb.input.partitionerOptions.partitionSizeMB", "64") \
            .option("spark.mongodb.input.partitionerOptions.numberOfPartitions", "30") \
            .load()
        
        df = df.repartition(6)
        df = df.persist(StorageLevel.DISK_ONLY)

        df.write.mode("overwrite") \
            .option("compression", "snappy") \
            .parquet(f"hdfs://namenode:9000/data/sales_db/orders/year={year}")

        print(f"Saved orders for {year}")


if __name__ == "__main__":
    extract_normal_collections()
    extract_orders_by_year()
    print("All collections extracted successfully.")
    spark.stop()
