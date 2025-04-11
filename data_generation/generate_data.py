from faker import Faker
import random
import uuid
from datetime import datetime, timedelta
from bson import ObjectId

fake =  Faker()

years = [2017,2018,2019,2020,2021,2022,2023,2024,2025]  #create year for random

def random_date():
    year = random.choice(years)
    start_date = datetime(year,1,1)
    end_date  = datetime(year,12,31,23,59,59)
    random_seconds = random.randint(0,int((end_date - start_date).total_seconds()))

    return start_date + timedelta(seconds=random_seconds)

def customers_gen():
    customer = {
        "_id": str(ObjectId()),
        "customer_name" : fake.name() if random.random() > 0.1 else None,
        "email" : fake.email() if random.random() > 0.2 else None,
        "phone_number" : fake.phone_number() if random.random() > 0.2 else None,
        "address" : {
            "street": fake.street_address() if random.random() > 0.15 else None,
            "city" : fake.city() if random.random() > 0.1 else None,
            "zip_code": fake.zipcode() if random.random() > 0.1 else None
            },
         "create_at" : random_date()
        }
    if customer["phone_number"] is None and customer["email"] is None:
            customer["phone_number"] = fake.phone_number() 

    return customer


def categories_gen():
    categories = [
    {"_id": str(ObjectId()), "category_name" : "Fashion", "description" : "Thời trang"},
    {"_id": str(ObjectId()), "category_name": "Electronics", "description": "Thiết bị điện tử công nghệ"},
    {"_id": str(ObjectId()), "category_name": "Furniture", "description" : "Đồ gia dụng, Nội thất"},
    {"_id": str(ObjectId()), "category_name" : "Beauty", "description" : "Làm đẹp"},
    {"_id": str(ObjectId()), "category_name" : "Sports", "description" : "Thể thao"},
    {"_id": str(ObjectId()), "category_name" : "Healths", "description" : "Sức khỏe"},
    {"_id": str(ObjectId()), "category_name" : "Appliances", "description" : "Thiết bị trong nhà"},
    {"_id": str(ObjectId()), "category_name" : "Toys", "description" : "Đồ chơi"},
    {"_id": str(ObjectId()), "category_name" : "Books", "description" : "Sách"}
    ] 
    return categories


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


def products_gen(product_categories):
    category = random.choice(list(product_categories.keys()))
    brand = random.choice(product_categories[category]["brands"])
    product_name = random.choice(product_categories[category]["products"])
    price = round(random.uniform(*product_categories[category]["prices"]), 2)
    stock_quantity = random.randint(0,500)
    rating = round(random.uniform(1.0,5.0),1)
    create_at = random_date()

    product = {
                "_id" : str(ObjectId()),
                "product_name": product_name,
                "brand": brand if random.random() > 0.1 else None,
                "category": category,
                "description": fake.sentence() if random.random() > 0.1 else None,
                "price": price if random.random() > 0.02 else None,
                "stock_quantity":stock_quantity,
                "rating": rating,
                "create_at" : create_at
        }
         
    return product


def suppliers_gen(brand):
    supplier={
            "_id": str(ObjectId()),
            "name":brand,
            "contact_person": fake.name(),
            "phone_number": fake.phone_number() if random.random() > 0.2 else None,
            "email": fake.email(),
            "address": fake.address()         
    }

    return supplier

def orders_gen(customers,products):
    customer = random.choice(customers)
    product = random.choices(products, k = random.randint(1,10))
    create_at = random_date()

    items = [{
                "product_id":item["_id"],
                "product_name":item["product_name"],
                "quantity": (qty := random.randint(1,10)) ,
                "price":item["price"],
                "total_price": qty*item["price"] if item["price"] is not None else 0
            } for item in product]
    
    order = {
            "_id": str(ObjectId()),
            "customer_id": customer["_id"],
            "order_date":create_at,
            "status": random.choice(["Completed","Canceled"]),
            "items": items,
            "total_amount": sum(item["total_price"] for item in items) if random.random() > 0.1 else None,
            "payment_method": random.choice(["Credit Card","Debit Cart","Cash","E-wallets","PayPal","Bank Card"]) if random.random() > 0.1 else None,
            "method": random.choice(["Expess","Buy in store"]) if random.random() > 0.2 else None, 
            "delivery_date": create_at if random.random() > 0.1 else None
        }
    
    return order



def inventory_gen(product):
    inventory={
            "_id": str(ObjectId()),
            "product_id" : product["_id"],
            "quantity_available": random.randint(1,1000),
            "last_updated": random_date()
        }
    
    return inventory

    
def employees_gen():
    positions = {
    "Sales": ["Sales Representative"] * 10 + ["Sales Manager"],  # 80% Employee, 20% Manager
    "Customer Service": ["Customer Service Representative"] * 5,  # 100% Employee
    "Marketing": ["Marketing Specialist"] * 4 + ["Marketing Manager"],  # 80% Employee
    "Warehouse": ["Inventory Specialist"] * 4 + ["Warehouse Manager"],  # 80% Employee
    "Finance": ["Finance Analyst"] * 4 + ["Finance Manager"],  # 80% Employee
    "HR": ["HR Specialist"] * 4 + ["HR Manager"]  # 80% Employee
    }

    departments = random.choice(list(positions.keys()))

    employee={
            "_id": str(ObjectId()),
            "employee_name": fake.name(),
            "postition": random.choice([positions[departments]]),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "hired_date": random_date()
        }
    
    return employee
       
    
    



        


      



