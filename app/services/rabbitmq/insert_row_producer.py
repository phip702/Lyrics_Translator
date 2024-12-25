import pika
import json

# def send_to_rabbitmq(queue_name, track_dict):
#     connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
#     channel = connection.channel()

#     # Declare the queue
#     channel.queue_declare(queue=queue_name, durable=True)

#     # Send the message to the queue
#     channel.basic_publish(
#         exchange='',
#         routing_key=queue_name,
#         body=json.dumps(track_dict),  # Use track_dict here
#         properties=pika.BasicProperties(
#             delivery_mode=2,  # Make the message persistent
#         )
#     )
#     print(f" [x] Sent message to {queue_name}")

# def insert_row_producer(track):
#     track_dict = track.to_dict()
#     send_to_rabbitmq('track_insert_queue', track_dict)

#TODO: make a less complicated example for testing to get producers and consumers working

def send_to_rabbitmq(queue_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue_name, durable=True)

    channel.basic_publish(
        exchange = '',
        routing_key = queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make the message persistent
        )
    )

    print(f' [X] Sent Testing Message ({message}) to Queue: {queue_name}')

def insert_row_producer(track):
    send_to_rabbitmq("Testing", track)

if __name__ == "__main__":
    insert_row_producer('HEYO')