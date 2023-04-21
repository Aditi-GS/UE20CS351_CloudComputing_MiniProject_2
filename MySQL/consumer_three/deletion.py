import pika
import mysql.connector

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

channel.exchange_declare(exchange='delete_exchange', exchange_type='direct')
# Declare the queue to listen for delete record requests
channel.queue_declare(queue='delete_queue')
channel.queue_bind(exchange='delete_exchange', queue='delete_queue', routing_key='delete')

# Define callback function to handle incoming messages
def callback(ch, method, properties, body):
    srn = body.decode('utf-8')
    # Delete record from the database
    sql = "DELETE FROM students WHERE SRN = %s"
    val = (srn,)
    cursor.execute(sql, val)
    db.commit()
    print("Record with SRN {} deleted".format(srn))
    # Acknowledge message received
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Listen for incoming messages on the queue
channel.basic_consume(queue='delete_queue', on_message_callback=callback)

print('Waiting for delete record requests...')
channel.start_consuming()
