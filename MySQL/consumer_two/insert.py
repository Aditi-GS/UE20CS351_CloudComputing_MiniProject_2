import pika
import mysql.connector

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

channel.exchange_declare(exchange='insert_exchange', exchange_type='direct')
# Declare the queue
channel.queue_declare(queue='insert_queue')
channel.queue_bind(exchange='insert_exchange', queue='insert_queue', routing_key='insert')

# Connect to MySQL database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="student_database"
)

cursor = db.cursor()

# Define a callback function to handle incoming messages
def callback(ch, method, properties, body):
    # Parse the data from the message
    data = body.decode('utf-8').split(',')
    name = data[0]
    srn = data[1]
    section = data[2]
    
    # Insert the data into the database
    sql = "INSERT INTO students (name, srn, section) VALUES (%s, %s, %s)"
    val = (name, srn, section)
    cursor.execute(sql, val)
    db.commit()
    
    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Start consuming messages
channel.basic_consume(queue='insert_queue', on_message_callback=callback)

print('Consumer Two (insert_record) started. Waiting for messages...')

# Start the event loop
channel.start_consuming()
