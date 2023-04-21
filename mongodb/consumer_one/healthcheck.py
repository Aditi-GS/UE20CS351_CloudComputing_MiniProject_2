import pika

# RabbitMQ connection details
# host name = rabbitmq container name running in rabbitmq_network
connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
channel = connection.channel()

# Declare the 'health_check' queue if it doesn't exist
channel.queue_declare(queue='health_check')

# Define a callback function to handle incoming messages
def callback(ch, method, properties, body):
    # Print the health check message received
    print("Received health check message: %r" % body)

    # Acknowledge the message received
    ch.basic_ack(delivery_tag=method.delivery_tag)
    return "Health check message receieved"

# Start consuming messages from the 'health_check' queue
channel.basic_consume(queue='health_check', on_message_callback=callback)

# Start consuming messages
print('Waiting for health check messages...')
channel.start_consuming()
