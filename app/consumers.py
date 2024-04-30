import pika


params = pika.URLParameters('amqps://csgaqrgu:kF83BEpmQIdLMXkSTYq6Y03VCiwDRAxj@moose.rmq.cloudamqp.com/csgaqrgu')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue = 'main')

def callback(ch, method, properties, body):
    print("Received in admin queue")
    print(body)

channel.basic_consume(queue='main', on_message_callback=callback)

print("\n\n\nStarted consuming")


channel.start_consuming()
channel.close()

