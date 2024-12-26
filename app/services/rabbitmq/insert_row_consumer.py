import pika
import json
from ...models import *  # Import the Track model
from ...extensions import db
from ...handlers.model_handlers import insert_row
from ...extensions import * #this imports db
from threading import Thread
import logging

#TODO: implement more complicated logic that has been commented out for producer and consumer
#* could implement Celery first as that can serialize object and then deserialize it on the other side for RabbitMQ; might not be better than my own custom .to_dict() methods

def consume_from_rabbitmq(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', heartbeat=60)) #consumer
    channel = connection.channel()    

    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        from ... import create_app #Putting this here avoids circular dependencies on app launch

        try:
            message_data = json.loads(body)  # Deserialize JSON to dictionary
            print(f" [x] Received: {message_data}")

            if queue_name == 'insert_track_queue':
                # Use the dictionary to create a Track object, or insert directly
                new_track = Track(
                    spotify_track_id=message_data['spotify_track_id'],
                    track_name=message_data['track_name'],
                    track_artist=message_data['track_artist'],
                    track_image=message_data.get('track_image')  # Optional field
                )
                app = create_app()
                with app.app_context():
                    insert_row(db, new_track)

            elif queue_name == 'insert_lyrics_queue':
                new_lyrics = Lyrics(
                    spotify_track_id=message_data['spotify_track_id'],
                    original_lyrics=message_data['original_lyrics'],
                    translated_lyrics=message_data['translated_lyrics'],
                    detected_language=message_data['detected_language']
                )
                app = create_app()
                with app.app_context():
                    insert_row(db, new_lyrics)

            # Acknowledge the message after successful processing
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logging.critical(f" [x] Message processed and acknowledged.")

        except Exception as e:
            print(f" [!] Error processing message: {e}")
            # Log the error to track the failure
            logging.error(f"Error processing message: {e}")
            # Optionally: Reject the message (without requeue) or nack with requeue
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
    channel.start_consuming() 

def start_consumer():
    # Create threads for consuming from each queue
    queues = ["insert_lyrics_queue", "insert_track_queue"]
    threads = []

    for queue in queues:
        thread = Thread(target=consume_from_rabbitmq, args=(queue,))
        thread.daemon = True  # Ensures that the threads are killed when the main program ends
        threads.append(thread)
        thread.start()

    # Optionally, wait for threads to finish (in a real application, you might want to handle termination signals)
    for thread in threads:
        thread.join()