import pika


params = pika.URLParameters('amqps://csgaqrgu:kF83BEpmQIdLMXkSTYq6Y03VCiwDRAxj@moose.rmq.cloudamqp.com/csgaqrgu')
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish():
    channel.basic_publish(exchange = '', routing_key = 'main', body = 'hello')

