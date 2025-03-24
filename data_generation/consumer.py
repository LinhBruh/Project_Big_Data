from confluent_kafka import Consumer
from pymongo import MongoClient
import json

conf = {
    "bootstrap.servers":"localhost:9093", #kafka broker
    "group.id": "bigdata-consumer-group", #create group consumer
    "auto.offset.reset": "earliest"   #to read first line of data
}

consumer = Consumer(conf)

consumer.subscribe(["orders"])
