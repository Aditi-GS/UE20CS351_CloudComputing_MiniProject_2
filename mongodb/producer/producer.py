from flask import Flask, request, jsonify
import pika
import json
import pymongo
from pymongo import MongoClient
client = MongoClient('mongodb')
db = client.mydatabase
records = db.records
# use pika for RabbitMQ connections

app = Flask(__name__)
@app.route('/health_check', methods=['GET'])
def health_check():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    except pika.exceptions.AMQPConnectionError as exc:
        print("Failed to connect to RabbitMQ service.")

    channel = connection.channel()
    # Send the health check message to the RabbitMQ queue
    message = request.args.get('message', 'RabbitMQ connection is established.')
    channel.queue_declare(queue='health_check')
    channel.basic_publish(exchange='', routing_key='health_check', body=message,properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    connection.close()
    print("Health check message sent to consumers")
    return 'Health check message sent to consumers.'


@app.route('/insert_record', methods=['POST'])
def insert_record():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    # Get the record details from the request
    record = {
        'name': request.form['name'],
        'srn': request.form['srn'],
        'section': request.form['section']
    }
    channel.queue_declare(queue='insert_record')
    channel.basic_publish(exchange='', routing_key='insert_record', body=json.dumps(record))
    connection.close()
    return 'Record inserted successfully.'

@app.route('/read_database', methods=['GET'])
def read_database():
    message = "read request sent"
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='read_database')
    channel.basic_publish(exchange='', routing_key='read_database', body=json.dumps(message),properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    return 'All records sent to consumers.'

@app.route('/delete_record', methods=['GET'])
def delete_record():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    # Get the SRN from the request
    srn = request.args.get('srn')
    # Delete the record from the database
    result = records.delete_one({'srn': srn})
    # Send the result to the RabbitMQ queue
    message = {'deleted_count': result.deleted_count}
    channel.basic_publish(exchange='', routing_key='delete_record', body=json.dumps(message),properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    return 'Deleted successfully'


app.run(host='0.0.0.0', port=5100, debug=True)
