import pika
import json
import pymongo
from pymongo import MongoClient

# connect to MongoDB
client = MongoClient('mongodb')

# get a reference to the database
db = client['mydatabase']

# get a reference to the collection
collection = db['students']

# callback function to handle incoming messages
def callback(ch, method, properties, body):
    # decode the message body from bytes to string
    message = body.decode('utf-8')

    # parse the message as JSON
    record = json.loads(message)

    # insert the record into the database
    collection.insert_one(record)

    # acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# connect to RabbitMQ and start consuming messages
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# declare the queue
channel.queue_declare(queue='insert_record', durable=True)

# set the prefetch count to 1
channel.basic_qos(prefetch_count=1)

# start consuming messages
channel.basic_consume(queue='insert_record', on_message_callback=callback)

print('Consumer Two (insert_record) started')
channel.start_consuming()
