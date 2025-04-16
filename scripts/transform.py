from pyspark.sql import SparkSession
import pyspark.sql.functions as func
from pyspark.sql.types import  StringType,StructField,StructType,IntegerType
from pyspark.sql.window import Window


spark = SparkSession.builder \
    .appName("TransformData") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS","hdfs://localhost:9000") \
    .getOrCreate()

collections = ["customers","products","orders"]
years = years = [2017,2018,2019,2020,2021,2022,2023,2024,2025]

def read_parquet(col):

    df = spark.read.parquet(f"hdfs://namenode:9000/data/sales_db/{col}/*.parquet")
    print(df.count())
    return df

def transform_data_customers():
        print(f"Begin with collection customers")
        df = read_parquet("customers")
        df.repartition(3)
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
            ) \
            .withColumn("customer_name",
                        func.when(func.col("customer_name").isNull(),"John Doe").otherwise(func.col("customer_name")) 
                        )\
            .withColumn(
                  "email",
                  func.when(func.col("email").isNull(),"johndoe@gmail.com").otherwise(func.col("email"))
            )\
            .withColumn(
                  "phone_number",
                  func.when(func.col("phone_number").isNull(),"0392306445").otherwise(func.col("phone_number"))
            )\
            .withColumn(
                "create_at",
                func.col("create_at").cast("date")
            )

        return  df


def transform_data_products():
        print("Begin with products")
        df = read_parquet("products")
        df.repartition(3)
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
                )\
                .withColumn(
                    "create_at",
                    func.col("create_at").cast("date")
                )
        return df


def transform_data_orders(year,price_df):
        print(f"Begin with order and year {year}")
        df = spark.read.parquet(f"hdfs://namenode:9000/data/sales_db/orders/year={year}")
        df.repartition(3)

        price_df = price_df.withColumnRenamed("price","new_price").withColumnRenamed("_id","product_id")

        df = df.alias("df").join(
                    price_df,
                    on = "product_id",
                    how = "left"
                )   

        df = df.cache()
        df.count()
 
        df =  df.withColumn(
                        "payment_method",
                        func.when(func.col("payment_method").isNull(),"Cash").otherwise(func.col("payment_method"))) \
                    .withColumn(
                        "method",
                        func.when(func.col("method").isNull(),"Buy in store").otherwise(func.col("method"))
                    ) \
                    .withColumn(
                        "date_key",
                        func.date_format(func.to_timestamp("order_date"),"yyyyMMdd")
                    )\
                    .withColumn(
                        "price",
                        func.when(func.col("price").isNull(),  func.col("new_price")).otherwise(func.col("price")) 
                    ).drop("new_price")\
                    .withColumn(
                        "total_price",
                        func.col("quantity") * func.col("price")
                    )\
                    .withColumnRenamed("_id","order_id")
        return df
                



    