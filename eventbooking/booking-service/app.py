from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import random
from flask_cors import CORS
import pika 
import json 
import os
# RabbitMQ Connection
# RABBITMQ_HOST = "localhost"
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
QUEUE_NAME = "notifications"

# def publish_notification(user_id, booking_id, message):
#     """Publishes a booking notification to RabbitMQ"""
#     try:
#         # connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
#         connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))

#         channel = connection.channel()
#         channel.queue_declare(queue=QUEUE_NAME, durable=True)

#         notification = {
#             "user_id": user_id,
#             "booking_id": booking_id,
#             "message": message
#         }

#         channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=json.dumps(notification))
#         connection.close()
#         print(f" Notification published for user {user_id}")
#     except Exception as e:
#         print(f" Error publishing to RabbitMQ: {e}")
def publish_notification(user_id, booking_id, message):
    try:
        print("📡 Connecting to RabbitMQ...")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        notification = {
            "user_id": user_id,
            "booking_id": booking_id,
            "message": message
        }

        print(f"📨 Sending: {notification}")
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=json.dumps(notification)
        )
        print("✅ Notification sent successfully.")
        connection.close()
    except Exception as e:
        print(f"❌ Failed to publish notification: {e}")


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# PostgreSQL Database Connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0434@localhost/bookingservice'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0434@host.docker.internal/bookingservice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Booking Model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    event_id = db.Column(db.String, nullable=False)  # Event ID (from Event Service MongoDB)
    status = db.Column(db.String(20), nullable=False, default="Pending")
    payment_status = db.Column(db.String(20), nullable=False, default="Pending")
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Ensure database tables are created
with app.app_context():
    db.create_all()

@app.route("/")
def health_check():
    return jsonify({"message": "Booking Service is running!"})


# EVENT_SERVICE_URL = "http://localhost:8080/api/events/"  # Update with actual Event Service URL
EVENT_SERVICE_URL = "http://host.docker.internal:8080/api/events/"

@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.json
    event_id = data.get("event_id")

    if not event_id:
        return jsonify({"error": "Event ID is required"}), 400

    # Use the correct Event Service URL (8080)
    event_response = requests.get(f"{EVENT_SERVICE_URL}{event_id}")

    if event_response.status_code != 200:
        return jsonify({"error": "Event not found"}), 404

    event_data = event_response.json()
    if event_data.get("capacity", 0) <= 0:
        return jsonify({"error": "Event is fully booked"}), 400

    # Create a new booking
    new_booking = Booking(user_id=data["user_id"], event_id=event_id)
    db.session.add(new_booking)
    db.session.commit()

    # decrese capacity 
    update_response = requests.put(f"{EVENT_SERVICE_URL}{event_id}/decrease_capacity")
    if update_response.status_code != 200:
        print("Failed to update event capacity:", update_response.json())  # Debugging log
        return jsonify({"error": "Failed to update event capacity"}), 500

    return jsonify({"booking_id": new_booking.id, "status": "Pending"}), 201




@app.route('/bookings', methods=['GET'])  #  Add GET request support
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([{
        "id": b.id,
        "user_id": b.user_id,
        "event_id": b.event_id,
        "status": b.status
    } for b in bookings])

@app.route('/payments', methods=['POST'])
def process_payment():
    data = request.json
    booking_id = data.get("booking_id")

    print("📣 in process payment")

    # Check if booking exists
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    # Simulate payment success or failure
    payment_success = random.choice([True, False])

    if payment_success:
        booking.payment_status = "Paid"
        booking.status = "Confirmed"  # Booking is confirmed after successful payment
        db.session.commit()
        print("📣 Sending notification to RabbitMQ")
        publish_notification(booking.user_id, booking.id, "Your booking has been confirmed!")

        return jsonify({"message": "Payment successful!", "booking_id": booking.id, "status": booking.status}), 200
    else:
        booking.payment_status = "Failed"
        db.session.commit()
        return jsonify({"message": "Payment failed. Please try again.", "booking_id": booking.id, "status": booking.status}), 400


#  Move `if __name__ == "__main__":` to the end
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
