from pyspark.sql import SparkSession
import pyspark.sql.functions as func
from pyspark.sql.types import StringType
from pyspark.sql.window import Window

# Tạo SparkSession
spark = SparkSession.builder \
    .appName("Local Word Count") \
    .master("local[*]") \
    .getOrCreate()

collections = ["inventory"]
# Load dữ liệu (có thể là file text)
def read_parquet(col):

    df = spark.read.parquet(f"hdfs://localhost:9000/data/sales_db/{col}")
    print(df.count())
    return df


def fill_null_customer_name(val):
    return val if val is not None else "John Doe"


def fill_null_email(val):
    return val if val is not None else "johndoe@gmail.com"

def fill_null_phone(val):
    return val if val is not None else "0123456789"


column_fill_func_customers ={
    "customer_name":fill_null_customer_name,
    "email":fill_null_email,
    "phone_number":fill_null_phone,
}
def transform_data():

    for col in  collections:
        print(f"Begin with collection {col}")
        df = read_parquet(col)
        df.repartition(3)
        if col == "products":
            window = Window.partitionBy("category")
            print(window)
            df = df.withColumn(
                "brand",
                func.when(
                    func.col("brand").isNull(),"No Brand").otherwise(func.col("brand").alias("brand"))
                ) \
                .withColumn("avg_price_by_category", func.avg("price").over(window)) \
                .withColumn(
                    "price",
                    func.when(func.col("price").isNull(),func.col("avg_price_by_category")).otherwise(func.col("price"))
                    )
                
        df.show(5)
df = read_parquet("inventory")
df.show(5)