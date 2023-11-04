import pika
import json
amqpUrl = 'amqps://paqrnanu:dlbW9DwIGgSOTd4TBF2bZLAWoTX2lRUX@vulture.rmq.cloudamqp.com/paqrnanu'

params = pika.URLParameters(amqpUrl)
connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    print(properties)
    msg_body = json.dumps(body)
    channel.basic_publish(
        exchange='', routing_key='email-service', body=msg_body, properties=properties)
