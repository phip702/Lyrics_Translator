import logging
import pika
import json
from ...models import *


def insert_row_producer(model_object):

    if type(model_object) == Track:
        track_dict = model_object.to_dict()
        send_to_rabbitmq('insert_track_queue', track_dict)

    elif type(model_object) == Lyrics:
        lyrics_dict = model_object.to_dict()
        send_to_rabbitmq('insert_lyrics_queue', lyrics_dict)

    else:
        logging.error(f"Unsupported object type: {type(model_object)}")

# def insert_row_producer(track):
#     send_to_rabbitmq("Testing", "HOLA") #* change second arg to track

#TODO: make a less complicated example for testing to get producers and consumers working

def send_to_rabbitmq(queue_name, message):
    # Create a connection with credentials as part of the connection parameters
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',
            port=5672,
            credentials=credentials
        )
    )
    
    channel = connection.channel()
    
    # Declare the queue
    channel.queue_declare(queue=queue_name, durable=True)

    # Send the message
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make the message persistent
        )
    )

    logging.critical(f' [X] Sent Testing Message ({message}) to Queue: {queue_name}')
    

def start_producer():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', heartbeat=60))
        channel = connection.channel()

        # Declare queues (durable to ensure messages are not lost)
        channel.queue_declare(queue='insert_track_queue', durable=True)
        channel.queue_declare(queue='insert_lyrics_queue', durable=True)

        # Producer logic without sending a message on startup
        print("Producer is ready but has not sent any message yet.")

        # Close the connection (no message is sent on startup)
        connection.close()

    except Exception as e:
        logging.error(f"Error in producer: {e}")

if __name__ == "__main__":
    for i in range(1,10):
        send_to_rabbitmq("Testing", f'HEYO=={i}')
    print('done')