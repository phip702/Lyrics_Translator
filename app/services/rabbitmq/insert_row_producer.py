import logging
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

def insert_row_producer(track):
    track_dict = track.to_dict()
    send_to_rabbitmq('insert_track_queue', track_dict)

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

    print(f' [X] Sent Testing Message ({message}) to Queue: {queue_name}')
    logging.critical(f' [X] Sent Testing Message ({message}) to Queue: {queue_name}')
    

def start_producer():
    logging.critical(f"MADE IT TO START_PRODUCER")
    send_to_rabbitmq("Testing", "PRODUCING ================")
    logging.critical(f"MADE IT TO SEND_TO_RABBITMQ=======")

if __name__ == "__main__":
    for i in range(1,10):
        send_to_rabbitmq("Testing", f'HEYO=={i}')
    print('done')