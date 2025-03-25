from confluent_kafka import Consumer
from pymongo import MongoClient
import json
import threading
import sys
import signal

conf = {
    "bootstrap.servers":"localhost:9093", #kafka broker
    "group.id": "bigdata-consumer-group", #create group consumer
    "auto.offset.reset": "earliest"   #to read first line of data
}



client_mongo = MongoClient("mongodb://admin:password@localhost:27017/")  #I need to create new user mongodb, check requirement or if you have mongodb in your computer, replace it
db = client_mongo["sales_db"] 
collections = {
    "customers" : db["customers"],
    "categories" : db["categories"],
    "products": db["products"],
    "suppliers": db["suppliers"],
    "orders" : db["orders"],
    "inventory" : db["inventory"],
    "employees": db["employees"]
}

def kafka_consumer(topics, collections, consumer_id):
    consumer = Consumer(conf)
    consumer.subscribe(topics)

    print(f"Consumer {consumer_id} started, listening to topics {topics}")

    datas = {topic : [] for topic in topics}  #create dict data for save to insert database

    while True:
        
        msg = consumer.poll(1.0) #wait 1.0s for takes messages from topic
        if msg is None:
            continue
        if msg.error():
            print(f"Error : {msg.error()}")
            continue

        topic = msg.topic()  #take the name of topic consumer is processing
        data = json.loads(msg.value().decode("utf-8"))  #decode data from topic
        datas[topic].append(data) #append data to dict

        if len(datas[topic]) > 100:
            try: 
                collections[topic].insert_many(datas[topic], ordered = False)  #insert data to collection
                print(f"Inserted {len(datas[topic])} records into {topic}") 
                datas[topic].clear() #clear list data after insert
            except Exception as e:
                print(f"Error insert {topic} : {e}")

    consumer.close()


topics = list(collections.keys())

threads = []
for i in range(10):
    t = threading.Thread(target=kafka_consumer,args=(topics,collections,i))  #create thread  
    t.start() #start it
    threads.append(t) #append thread
for t in threads:
    t.join() #join one by one to 10 thread run the same time
    



    





