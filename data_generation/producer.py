from confluent_kafka import Producer
import json
import time
import generate_data as gd
from multiprocessing import Pool, cpu_count
import uuid


def create_producer():
    conf = {
        "bootstrap.servers":"localhost:9093", #location Kafka broker
        "linger.ms":100, #if have less messages, Kafka will wait 100ms to before sent messages(increase performance)
        "client.id":"bigdata-producer", #create name client producer(help easier debug)
        "batch.num.messages":1000 #send maximum 1000 messages for a batch
    }
    return Producer(conf)


def delivery_report(err,msg):
    if err is not None:
        print(f"Message delivery failed {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def send_message_to_kafka(topic,messages):
    producer = create_producer()
    for message in messages:
        producer.produce(
            topic,  #topic need to send message
            key = str(uuid.uuid4()), #create random key for partition
            value = json.dumps(message, default=str), #convert dict to json
            callback = delivery_report #call callback to check status send message
        )
    producer.flush() #ensure all data have sent
 
def chunk_list(data, size):   #Because I create list data so need to create a function to chunk data of list to smaller for process
    for i in range(0, len(data), size):
        yield data[i:i + size]


number_customers = 100000
number_products = 50000
number_orders = 10_000_000
number_employees = 1000



brands = []
for key in list(gd.product_categories.keys()):
    brands = brands + gd.product_categories[key]["brands"]


customers = [gd.customers_gen() for _ in range(number_customers)]
categories = gd.categories_gen()
products = [gd.products_gen(gd.product_categories) for _ in range(number_products)]
suppliers = [gd.suppliers_gen(brands[i]) for i in range(len(brands))]
inventory = [gd.inventory_gen(products[i]) for i in range(number_products)]
employees = [gd.employees_gen() for _ in range(number_employees)]

def send_orders(batch_size = 1000):                     
    orders = [gd.orders_gen(customers, products) for _ in range(batch_size)]
    send_message_to_kafka("orders",orders)

if __name__ == "__main__":
    number_worker = min(cpu_count(),9)

    with Pool(number_worker) as p :
        p.starmap(send_message_to_kafka,[("customers", batch) for batch in chunk_list(customers, 1000)])
        p.starmap(send_message_to_kafka,[("products", batch) for batch in chunk_list(products, 1000)])
        p.starmap(send_message_to_kafka,[("inventory", batch) for batch in chunk_list(inventory, 1000)])


        send_message_to_kafka("categories",categories)
        send_message_to_kafka("suppliers",suppliers)
        send_message_to_kafka("employees",employees)

        #divide order follow batch size (void to Kafka fault for overload)
        batch_sizes = [1000] * (number_orders // 1000)
        p.map(send_orders, batch_sizes)
