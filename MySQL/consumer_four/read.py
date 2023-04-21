import pika
import mysql.connector
import json

# Connect to MySQL database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="student_database"
)

cursor = db.cursor()

# RabbitMQ connection details
# Gateway IP Address
rabbitmq_host="rabbitmq"
rabbitmq_port = 15672
rabbitmq_user = 'guest'
rabbitmq_password = 'guest'

# Create a RabbitMQ connection and channel
rabbitmq_credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=rabbitmq_credentials))
channel = connection.channel()

channel.exchange_declare(exchange='read_exchange', exchange_type='direct')
# Declare the queue
channel.queue_declare(queue='read_queue')
channel.queue_bind(exchange='read_exchange', queue='read_queue', routing_key='read')

# Define a callback function to process the message
def callback(ch, method, properties, body):
    # Retrieve all records from database
    if body == 'Read database':
        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()
        
    # Convert records to JSON format
    result = []
    for record in records:
        result.append({
            'name': record[0],
            'srn': record[1],
            'section': record[2]
        })
    result_json = json.dumps(result)
    
    # Print the result
    print(result_json)
    
    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Start consuming messages from the queue
channel.basic_consume(queue='read_queue', on_message_callback=callback)

print('Waiting for messages...')
channel.start_consuming()
