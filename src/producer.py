import pika
import json
import os
from dotenv import load_dotenv
load_dotenv()

amqpUrl = os.getenv('AMQPURL')

params = pika.URLParameters(amqpUrl)
connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    print(channel.is_closed)
    properties = pika.BasicProperties(method)
    print(properties)
    msg_body = json.dumps(body)
    channel.basic_publish(
        exchange='', routing_key='email-service', body=msg_body, properties=properties)
