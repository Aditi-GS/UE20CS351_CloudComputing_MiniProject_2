from flask import Flask, jsonify, request
# pika lib to interact with RabbitMQ
import pika

app = Flask(__name__)

# Create a RabbitMQ connection and channel
# host name = rabbitmq container name running in rabbitmq_network
connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
channel = connection.channel()

# Create an exchange and queues for each consumer 
# msgs aren't sent to the queues directly 
# exchanges route specified msgs to their respective queues --- based on routing/binding keys
# exchange type = direct ---> msgs are sent only according to their routing keys
channel.exchange_declare(exchange='insert_exchange', exchange_type='direct')
channel.exchange_declare(exchange='read_exchange', exchange_type='direct')
channel.exchange_declare(exchange='delete_exchange', exchange_type='direct')
channel.exchange_declare(exchange='health_check_exchange', exchange_type='direct')

channel.queue_declare(queue='insert_queue')
channel.queue_declare(queue='read_queue')
channel.queue_declare(queue='delete_queue')
channel.queue_declare(queue='health_check')

# Bind queues to exchanges
channel.queue_bind(exchange='insert_exchange', queue='insert_queue', routing_key='insert')
channel.queue_bind(exchange='read_exchange', queue='read_queue', routing_key='read')
channel.queue_bind(exchange='delete_exchange', queue='delete_queue', routing_key='delete')
channel.queue_bind(exchange='health_check_exchange', queue='health_check', routing_key='health_check')

# Health check endpoint
@app.route('/health_check', methods=['GET'])
def health_check():
    # Publish message to health check queue
    message = request.args.get('message', 'Health check')
    channel.basic_publish(exchange='health_check_exchange', 
                            routing_key='health_check', 
                            body=message
                        )
    return 'Message sent to health_check queue'

# Insert record endpoint
@app.route('/insert', methods=['POST'])
def insert_data():
    name = request.form['Name']
    srn = request.form['SRN']
    section = request.form['Section']
    message = f'{name},{srn},{section}'
    channel.basic_publish(exchange='insert_exchange', 
                            routing_key='insert', 
                            body=message
                        )
    return 'Message sent to insert_queue'

# Read Database endpoint
@app.route('/read_database', methods=['GET'])
def read_database():
    # Send message to all read queues
    channel.basic_publish(exchange='read_exchange', 
                            routing_key='read', 
                            body='Read database'
                        )
    return 'Message sent to read queues'

# Delete record endpoint
@app.route('/delete_record', methods=['GET'])
def delete_record():
    srn = request.args.get('SRN')
    message = srn
    channel.basic_publish(exchange='delete_exchange', 
                            routing_key='delete', 
                            body=message
                        )
    return 'Message sent to delete_queue'

if __name__ == '__main__':
    # port for health check endpoint
    app.run(host='0.0.0.0', port=5000)
    # port for insert endpoint
    app.run(host='0.0.0.0', port=5001)
    # port for read endpoint
    app.run(host='0.0.0.0', port=5002)
    # port for delete endpoint 
    app.run(host='0.0.0.0', port=5003)
