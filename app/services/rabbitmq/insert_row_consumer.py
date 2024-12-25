import pika
import json
from ...models import Track  # Import the Track model
from ...extensions import db
from ...handlers.model_handlers import insert_row

# def consume_from_rabbitmq():
#     connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
#     channel = connection.channel()

#     # Declare the queue with durable=True to match the producer
#     channel.queue_declare(queue='track_insert_queue', durable=True)

#     def callback(ch, method, properties, body):
#         try:
#             track_data = json.loads(body)  # Deserialize JSON to dictionary
#             print(f" [x] Received: {track_data}")

#             # Use the dictionary to create a Track object, or insert directly
#             new_track = Track(
#                 spotify_track_id=track_data['spotify_track_id'],
#                 track_name=track_data['track_name'],
#                 track_artist=track_data['track_artist'],
#                 track_image=track_data.get('track_image')  # Optional field
#             )

#             # Insert the new_track object into the database
#             db.session.add(new_track)
#             db.session.commit()

#             # Acknowledge the message after successful processing
#             ch.basic_ack(delivery_tag=method.delivery_tag)
#             print(" [x] Message processed and acknowledged.")
#         except Exception as e:
#             print(f" [!] Error processing message: {e}")
#             # Optionally: Don't acknowledge so the message can be retried
#             # ch.basic_nack(delivery_tag=method.delivery_tag)

#     channel.basic_consume(queue='track_insert_queue', on_message_callback=callback, auto_ack=False)
#     print(" [*] Waiting for messages. To exit press CTRL+C")
#     channel.start_consuming()

def consume_from_rabbitmq(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()    

    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        print(" [x] Received:", body)

    channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,  # Here is where the callback is passed
    auto_ack=True
    )  

    channel.start_consuming()

if __name__ == "__main__":
    consume_from_rabbitmq("Testing")