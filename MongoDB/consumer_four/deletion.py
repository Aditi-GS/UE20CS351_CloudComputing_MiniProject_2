import pika
from pymongo import MongoClient

# Set up connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmqd'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='delete_record', durable=True)


# Function to delete a record from MongoDB based on SRN
def delete_record(srn):
    client = MongoClient('mongodb')
    db = client['mydatabase']
    collection = db['students']
    query = {'srn': srn}
    result = collection.delete_one(query)
    return result.deleted_count


# Function to process incoming messages from RabbitMQ
def callback(ch, method, properties, body):
    srn = body.decode('utf-8')
    result = delete_record(srn)
    print(f"Deleted {result} record(s) with SRN '{srn}'")


# Start consuming messages from the queue
channel.basic_consume(queue='delete_record', on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()
