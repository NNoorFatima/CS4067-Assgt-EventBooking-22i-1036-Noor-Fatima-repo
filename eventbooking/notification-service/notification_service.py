import threading
import pika
import json
import os
from flask import Flask, jsonify
from pymongo import MongoClient
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId  # Import this to convert MongoDB ObjectId



MONGO_URI = "mongodb+srv://Event-Service:123@cluster0.ieune.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Flask App
app = Flask(__name__)

# MongoDB Atlas Connection
client = MongoClient(MONGO_URI)
db = client["notification_service"]
notifications_collection = db["notifications"]

# RabbitMQ Connection
RABBITMQ_HOST = "localhost"
QUEUE_NAME = "notifications"

def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    return connection, channel

# Function to Handle Received Messages
def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f" [x] Received: {message}")
    
    notification = {
        "user_id": message["user_id"],
        "booking_id": message["booking_id"],
        "message": message["message"],
        "timestamp": datetime.utcnow(),
        "read": False
    }
    
    # Store notification in MongoDB
    notifications_collection.insert_one(notification)
    print(f" Notification stored for user {message['user_id']}")
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

# RabbitMQ Consumer
def start_rabbitmq_consumer():
    connection, channel = connect_to_rabbitmq()
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    print(" [*] Waiting for messages from RabbitMQ. To exit press CTRL+C")
    channel.start_consuming()

# Run RabbitMQ Consumer in a Separate Thread
def run_consumer_thread():
    consumer_thread = threading.Thread(target=start_rabbitmq_consumer)
    consumer_thread.daemon = True
    consumer_thread.start()

# Start Consumer when Flask App Starts
run_consumer_thread()

# API to Fetch Notifications for a User
@app.route("/notifications/<user_id>", methods=["GET"])
def get_notifications(user_id):
    """Retrieve all notifications for a given user ID"""
    
    # 🔹 Ensure user_id is treated as INT if needed
    try:
        user_id = int(user_id)  # Convert to integer
    except ValueError:
        pass  # Keep it as string if conversion fails

    notifications = list(notifications_collection.find({"user_id": user_id}, {"_id": 0}))
    
    return jsonify(notifications), 200

# Run Flask App
if __name__ == "__main__":
    app.run(port=5003, debug=True)
