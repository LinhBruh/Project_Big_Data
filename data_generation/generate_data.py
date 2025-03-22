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

def random_null(value):
    return value if random.random() > 0.15 else None

def customers_gen():
    number_customer = 5_00_000
    customers = []
    for i in range(number_customer):
        customers.append({
        "_id": str(uuid.uuid4()),
        "customer_id" : f"CUST00{i}",
        "customer_name" : fake.name(),
        "email" : fake.email(),
        "phone_number" : fake.phone_number(),
        "address" : {
            "street": fake.street_address(),
            "city" : fake.city(),
            "zip_code": fake.zipcode()
        },
         "create_at" : random_date().strftime("%Y-%m-%d %H:%M:%S")
    })

    customers_df = pd.DataFrame(customers)
    columns = list(customers_df.columns)
    for col in columns:
        customers_df[col]=customers_df[col].apply(random_null)
    customers_df.to_csv("./data_generation/customers.csv")
    return customers

customers = customers_gen()

categories_collection = db["categories"]
def categories_gen():
    categories = [
    {"_id": str(uuid.uuid4()),"category_id": "CAT001", "category_name" : "Fashion", "description" : "Thời trang"},
    {"_id": str(uuid.uuid4()),"category_id": "CAT002", "category_name": "Electronics", "description": "Thiết bị điện tử công nghệ"},
    {"_id": str(uuid.uuid4()),"category_id": "CAT003", "category_name": "Furniture", "description" : "Đồ gia dụng, Nội thất"},
    {"_id": str(uuid.uuid4()),"category_id": "CAT004", "category_name" : "Beauty", "description" : "Làm đẹp"},
    {"_id": str(uuid.uuid4()),"category_id": "CAT005", "category_name" : "Sports", "description" : "Thể thao"},
    {"_id": str(uuid.uuid4()),"category_id": "CAT006", "category_name" : "Healths", "description" : "Sức khỏe"},
    {"_id": str(uuid.uuid4()),"category_id": "CAT007", "category_name" : "Appliances", "description" : "Thiết bị trong nhà"},
    {"_id": str(uuid.uuid4()),"category_id": "CAT008", "category_name" : "Toys", "description" : "Đồ chơi"},
    {"_id": str(uuid.uuid4()),"category_id": "CAT009", "category_name" : "Books", "description" : "Sách"}
    ]
    categories_df = pd.DataFrame(categories)
    categories_df.to_csv("./data_generation/categories.csv")
    return categories

categories = categories_gen()

products_collection = db["products"]
product_categories ={
    "Fashion":{
        "brands": ["Luis Vuiton","Dior","OWEN","CoolMate","CANIFA","Adidas","Puma","Nike","Zara","H&M"],
        "products": ["T-shirt","Jean","Jacket","Sneakers","Hat","Gloves","Sweater","Shirt","Trousers","Dress","Tank Top","Skirt","Coat"],
        "prices" : (10,200)
    },
    "Electronics":{
        "brands": ["Apple","SamSung","Sony","LG","Dell","HP","BlackBerry","Acer","Xiaomi","Vsmart"],
        "products": ["Laptop","Smartphone","PC","Tablet","Smartwatch","Headphones"],
        "prices":(200,4000)
    },
    "Furniture":{
        "brands": ["IEKA","Asley Furniture","La-Z-Boy","Aeron","Harvey Norman","Forma Ideale"],
        "products":["Table","Chair","Sofa","Bed","Cabinet","Fan","Lamp","Bookshelf","Clock"],
        "prices": (10,2000)
    },
    "Beauty":{
        "brands":["Coccon","Decuma","Cosmetic","Beauty Box","Bihacu","CoCoLux"],
        "products":["Lipstick","Mascara","Cleanser","Scrub","Foundation","Cushion","Sponge","Hightlighter","Contour","Brush","Lip balm","Hair spray"],
        "prices": (10,500)
    },
    "Sports":{
        "brands":["Nike","Adidas","Puma","New Balance","Fila","Champion","Lascoste"],
        "products":["Swim gear","Running clothes","Yoga wear","Hiking gear","Football kit","Ski wear","Cycling clothes"],
        "prices":(100,3000)
    },
    "Healths":{
        "brands":["Pharmacy","Traphaco","Imexfarm","Domesco","Pymepharco","OPC"],
        "products": ["Aspirin","Capsule","Ibuprofen","Generic","Vitamin","Analgesic","Antihistamin","Antivirus","Antipyretic","Sedative","Statin","Vaccin","Decongestant"],
        "prices":(10,200)
    },
    "Appliances":{
        "brands": ["LG","Xiaomi","SamSung","Philips","Panasonic","Inverter","Toshiba","AQUA"],
        "products":["Washing Machine","Dishwasher","Microwave","Air condistioner","Blender","Refrigerator","Fryer","Induction cooktop","Vacuum cleaner","Robot mop"],
        "prices":(500,10_000)
    },
    "Toys":{
        "brands":["Lego","Masttel","Hasbro"],
        "products": ["Lego set","Doll","Puzzle","RC car","Board game"],
        "prices": (5,500)
     },
    "Books":{
        "brands":["Penguin","HarperCollins","Oxford","Scholastic","Fahasa","VinaBook","NhaNam"],
        "products": ["Fiction Book", "Science Book", "History Book", "Self-help Book","Detective Books","Bussiness Book","School Book"],
        "prices":(1,100)
    }
}
def products_gen():
    num_product = 50_000
    products = []
    for i in range(num_product):
        category = random.choice(list(product_categories.keys()))
        brand = random.choice(product_categories[category]["brands"])
        product_name = random.choice(product_categories[category]["products"])
        price = round(random.uniform(*product_categories[category]["prices"]), 2)
        stock_quantity = random.randint(0,500)
        rating = round(random.uniform(1.0,5.0),1)
        create_at = random_date().strftime("%Y-%m-%d %H:%M:%S")
        products.append(
            {
                "_id":str(uuid.uuid4()),
                "product_id" : f"PRO00{i}",
                "product_name": product_name,
                "brand": brand,
                "category": category,
                "price": price,
                "stock_quantity":stock_quantity,
                "rating": rating,
                "create_at" : create_at
            }
        )
    product_df = pd.DataFrame(products)
    columns = list(product_df.columns)
    for col in columns:
        product_df[col] = product_df[col].apply(random_null)
    product_df.to_csv("./data_generation/products.csv")
    return products
    
products = products_gen()

suppliers_collection = db["suppliers"]
def suppliers_gen():
    suppliers = []
    categories = list(product_categories.keys())
    brands = []
    for key in categories:
        brands += product_categories[key]["brands"]
    for i in range(len(brands)):
        suppliers.append({
            "_id": str(uuid.uuid4()),
            "supplier_id": f"SUP00{i}",
            "name":brands[i],
            "contact_person": fake.name(),
            "phone_number": fake.phone_number(),
            "email": fake.email(),
            "address": fake.address()         
        })
    suppliers = pd.DataFrame(suppliers)
    suppliers.to_csv("./data_generation/suppliers.csv")
    return suppliers

suppliers = suppliers_gen()

orders_collection = db["orders"]
def orders_gen():
    number_orders = 100_000_000
    orders = []
    for i in range(number_orders):
        customer = random.choice(customers)
        product = random.choices(products, k = random.randint(1,10))
        create_at = random_date()
        items = [{
                "product_id":item["product_id"],
                "product_name":item["product_name"],
                "quantity": (qty := random.randint(1,10)) ,
                "price":item["price"],
                "total_price": qty*item["price"]
            } for item in product],
        orders.append({
            "_id":str(uuid.uuid4()),
            "order_id": f"ORD00{i}",
            "customer_id": customer["customer_id"],
            "order_date":create_at,
            "status": random.choice(["Completed","Canceled"]),
            "items": items,
            "total_amount": sum(item["total_price"] for item in items),
            "payment_method": random.choice(["Credit Card","Debit Cart","Cash","E-wallets","PayPal","Bank Card"]),
            "method": random.choice(["Expess","Buy in store"]), 
        })
    orders_df = pd.DataFrame(orders)
    columes = list(orders_df.columns)
    for col in columes:
        orders_df[col] = orders_df[col].apply(random_null) 
    orders_df.to_csv("./data_generation/orders.csv")
    return orders

orders = orders_gen()

inventory_collection = db["inverntory"]
def inventory_gen():
    inventory = []
    for i in range(int(len((products)))):
        inventory.append({
            "_id": str(uuid.uuid4()),
            "inventory_id": f"INV00{i}",
            "product_id" : products[i]["product_id"],
            "quantity_available": random.randint(1,1000),
            "last_updated": random_date()
        })
    inventory_df = pd.DataFrame(inventory)
    inventory_df.to_csv("./data_generation/inventory.csv")

inventory_gen()

payments_collection = db["payments"]
def payments_gen():
    payments = []
    for i in range(1,len(orders)+1):
            payments.append({
                "_id":str(uuid.uuid4()),
                "payment_id":f"PAY00{i}",
                "order_id": orders[i]["order_id"],
                "custiomer_id": orders[i]["customer_id"],
                "amount": orders[i]["total_amount"],
                "payment_date":orders[i]["order_date"],
                "payment_method":orders[i]["payment_method"],
                "status": orders[i]["status"]
            })
    payments_df = pd.DataFrame(payments)
    payments_df.to_csv("./data_generation/payments.csv")

payments_gen()

employees_collection = db["employees"]
def employees_gen():
    positions = {
    "Sales": ["Sales Representative"] * 10 + ["Sales Manager"],  # 80% Employee, 20% Manager
    "Customer Service": ["Customer Service Representative"] * 5,  # 100% Employee
    "Marketing": ["Marketing Specialist"] * 4 + ["Marketing Manager"],  # 80% Employee
    "Warehouse": ["Inventory Specialist"] * 4 + ["Warehouse Manager"],  # 80% Employee
    "Finance": ["Finance Analyst"] * 4 + ["Finance Manager"],  # 80% Employee
    "HR": ["HR Specialist"] * 4 + ["HR Manager"]  # 80% Employee
    }
    
    number_employees = 1000
    employees = []
    for i in range(1,number_employees + 1):
        departments = random.choice(list(positions.keys()))
        employees.append({
            "_id": str(uuid.uuid4()),
            "employee_id": f"EMP00{i}",
            "employee_name": fake.name(),
            "postition": random.choice[positions[departments]],
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "hired_date": random_date()   
        })
    employees_df = pd.DataFrame(employees)
    employees_df.to_csv("./datageneration/employees.csv")

employees_gen()
    
    



        


      



