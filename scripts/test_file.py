from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from pyspark.sql.window import Window
from pyspark.sql.types import StructField,StructType,IntegerType,StringType
import transform

spark  =  SparkSession.builder \
        .appName("Load to JDBC")\
        .master("spark://spark-master:7077") \
        .config("spark.postgres.url","jdbc:postgresql://@postgresql:5432/dw_sales") \
        .config("spark.postgres.user","admin") \
        .config("spark.postgres.password","password") \
        .config("spark.jars","/opt/spark/jars/postgresql-42.7.1.jar") \
        .getOrCreate()
schema1 = StructType([
        StructField("_id",StringType(),True),
        StructField("price",IntegerType(),True)
    ])
schema2 = StructType([
        StructField("category_name",StringType(),True),
        StructField("product_id",StringType(),True)
    ])

df_product = transform.transform_data_products()

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
    
df = transform.transform_data_orders(2017,price_df)
        
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
df = df.withColumnRenamed("order_date","create_at")
df.show(5)
df.printSchema()