import pika
import json

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "notifications"

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# Declare queue
channel.queue_declare(queue=QUEUE_NAME, durable=True)

# Create a test notification message
message = json.dumps({
    "booking_id": "12345",
    "user_id": "987",
    "message": "Your booking has been confirmed!"
})

# Publish message to RabbitMQ
channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)

print("✅ Test message sent to RabbitMQ!")
connection.close()
