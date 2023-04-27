import pymongo
import pika
import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb')
db = client["mydatabase"]
collection = db["students"]

# RabbitMQ connections
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='read_database', durable=True)

def callback(ch, method, properties, body):
    print("Received request to read database...")
    
    # Retrieve all records from database
    records1 = []
    for doc in collection.find():
        records1.append(doc)
    for x in records1:
        print(x)
        
   # Retrieve all the records of a specific SRN from the database
    records2 = []
    for doc in collection.find({'SRN':'78'}):
        records2.append(doc)
    for x in records2:
        print(x)

    
    # Send records back as response
    response = json.dumps(records)
    ch.basic_publish(exchange='', routing_key=properties.reply_to, properties=pika.BasicProperties(correlation_id = \
                      properties.correlation_id), body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Listen to "read_database" queue
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='read_database', on_message_callback=callback)

print('Waiting for requests to read database...')
channel.start_consuming()
