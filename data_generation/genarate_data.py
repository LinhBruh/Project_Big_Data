import pandas as pd 
from faker import Faker
import numpy
from pymongo import MongoClient
import random
import uuid
from datetime import datetime, timedelta

fake =  Faker()
client = MongoClient("mongodb://admin:password@localhost:27017/")

db = client["sales_db"]
customers_collection = db["customers"]

years = [2017,2018,2019,2020,2021,2022,2023,2024,2025]
def random_date():
    year = random.choice(years)
    start_date = datetime(year,1,1)
    end_date  = datetime(year,12,31,23,59,59)

    random_seconds = random.randint(0,int((end_date - start_date).total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

number_customer = 100000

customers = []

# for i in range(1,number_customer+1):
#     customers.append({
#         "customer_id" : str(uuid.uuid4()),
#         "customer_name" : fake.name(),
#         "email" : fake.email(),
#         "phone_number" : fake.phone_number(),
#         "address" : {
#             "street": fake.street_address(),
#             "city" : fake.city(),
#             "zip_code": fake.zipcode()
#         },
#          "create_at" : random_date().strftime("%Y-%m-%d %H:%M:%S")
#     })

customers = pd.read_csv(".\customers.csv")
print(customers["customer_id"])

