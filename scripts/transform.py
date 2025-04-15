from pyspark.sql import SparkSession
import pyspark.sql.functions as func
from pyspark.sql.types import  StringType
from pyspark.sql.window import Window
spark = SparkSession.builder \
    .appName("TransformData") \
    .master("spark://local[*]") \
    .config("spark.hadoop.fs.defaultFS","hdfs://localhost:9000") \
    .getOrCreate()

collections = ["customers","products","inventory"]

def read_parquet(col):

    df = spark.read.parquet(f"hdfs://namenode:9000/sales_db/{col}/*.parquet")
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
        if col == "customers":
            df = df.withColumn(
                "address",
                func.struct(
                    func.col("address.street").alias("street"),
                    func.when(
                        func.col("address.city").isNull(), "VietNam"
                    ).otherwise(
                        func.col("address.city")
                    ).alias("city"),
                    func.col("address.zip_code").alias("zip_code")
                )
            )
        for column in df.columns:
            if column in column_fill_func_customers:
                df = df.withColumn(column, column_fill_func_customers[column](func.col(column)))
        
        if col == "products":
            window = Window.partitionBy("category")
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
        if col == "orders":
            


    