from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from pyspark.sql.window import Window
from pyspark.sql.types import StructField,StructType,IntegerType,StringType
import transform

spark  =  SparkSession.builder \
        .appName("Load to JDBC")\
        .master("spark://spark-master:7077")\
        .config("spark.postgres.url","jdbc:postgresql://@postgresql:5432/dw_sales")\
        .config("spark.postgres.user","admin")\
        .config("spark.postgres.password","password")\
        .config("spark.jars","/opt/spark/jars/postgresql-42.7.1.jar")\
        .getOrCreate()

df_customer  = transform.transform_data_customers()
df_product =transform.transform_data_products()

def load_dimension(df_product,df_customer):
    

    df_customer = df_customer.select(func.col("_id"),func.col("customer_name"),func.col("sex"),func.col("phone_number"),func.col("email"),func.col("address.city").alias("city"),func.col("create_at"))
    df_customer = df_customer.withColumnRenamed("_id","customer_id")
    df_customer = df_customer.cache()
    df_customer.count()

    df_customer.write.format("jdbc")\
                .option("url","jdbc:postgresql://postgresql:5432/dw_sales")\
                .option("dbtable","dim_customers")\
                .option("user","admin")\
                .option("password","password")\
                .option("driver", "org.postgresql.Driver")\
                .mode("append")\
                .save()
    
    df_product_load = df_product.select(func.col("_id"),func.col("product_name"),func.col("rating"),func.col("stock_quantity").alias("quantity"),func.col("price"),func.col("brand"),func.col("create_at"))
    df_product_load = df_product_load.withColumnRenamed("_id","product_id")
    df_product_load = df_product_load.cache()
    df_product_load.count()

    df_product_load.write.format("jdbc")\
                .option("url","jdbc:postgresql://postgresql:5432/dw_sales")\
                .option("dbtable","dim_products")\
                .option("user","admin")\
                .option("password","password")\
                .option("driver", "org.postgresql.Driver")\
                .mode("append")\
                .save()
    
    df_categories = df_product.select("category", "create_at")\
        .withColumn("rank", func.row_number().over(Window.partitionBy("category").orderBy("create_at")))\
        .filter("rank = 1")\
        .drop("rank")\
        .withColumnRenamed("category", "category_name")
    df_categories.write.format("jdbc")\
                .option("url","jdbc:postgresql://postgresql:5432/dw_sales")\
                .option("dbtable","dim_categories")\
                .option("user","admin")\
                .option("password","password")\
                .option("driver", "org.postgresql.Driver")\
                .mode("append")\
                .save()
  
def load_fact(df_product):
    schema1 = StructType([
        StructField("_id",StringType(),True),
        StructField("price",IntegerType(),True)
    ])
    schema2 = StructType([
        StructField("category_name",StringType(),True),
        StructField("product_id",StringType(),True)
    ])

    price_df = spark.createDataFrame([],schema1)
    price_df = df_product.select("_id","price")
    df_cat_prd = spark.createDataFrame([],schema2)
    df_cat_prd = df_product.select("category","_id").withColumnRenamed("_id","product_id").withColumnRenamed("category","category_name")

    df_cat= spark.read.format("jdbc")\
                .option("url","jdbc:postgresql://postgresql:5432/dw_sales")\
                .option("dbtable","(SELECT category_key, category_name FROM dim_categories) AS dim_cat")\
                .option("user","admin")\
                .option("password","password")\
                .option("driver", "org.postgresql.Driver")\
                .load()
        
    df_prd=spark.read.format("jdbc")\
                .option("url","jdbc:postgresql://postgresql:5432/dw_sales")\
                .option("dbtable","(SELECT product_key, product_id FROM dim_products) AS dim_prd")\
                .option("user","admin")\
                .option("password","password")\
                .option("driver", "org.postgresql.Driver")\
                .load()
        
    df_cus=spark.read.format("jdbc")\
                .option("url","jdbc:postgresql://postgresql:5432/dw_sales")\
                .option("dbtable","(SELECT customer_key, customer_id FROM dim_customers) AS dim_cus")\
                .option("user","admin")\
                .option("password","password")\
                .option("driver", "org.postgresql.Driver")\
                .load()
    df_cat = df_cat.join(
        df_cat_prd,
        on="category_name",
        how="left"
    )
    for year in range(2017,2026):
        print(f"Begin with orders year = {year}")
        df = transform.transform_data_orders(year,price_df)
        
        df = df.alias("df").join(
             df_prd,
             on = "product_id",
             how="left"
        )
        
        df = df.join(
            df_cat,
            on="product_id",
            how="left"
        )

        df = df.join(
            df_cus,
            on="customer_id",
            how="left"
        )

        df = df.select("order_id","category_key","product_key","customer_key","date_key","method","payment_method","total_price","quantity","status","order_date")
        df = df.withColumnRenamed("order_date","create_at").withColumn("date_key",func.col("date_key").cast("int"))
        df = df.na.drop()

        df.write.format("jdbc")\
                .option("url","jdbc:postgresql://postgresql:5432/dw_sales")\
                .option("dbtable","fact_orders")\
                .option("user","admin")\
                .option("password","password")\
                .option("driver", "org.postgresql.Driver")\
                .mode("append")\
                .save()
    
load_dimension(df_product,df_customer)
load_fact(df_product)

