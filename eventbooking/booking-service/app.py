from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

# PostgreSQL Database Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0434@localhost/bookingservice'
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

# ✅ Move this above `if __name__ == "__main__":`
EVENT_SERVICE_URL = "http://localhost:8080/api/events/"  # Update with actual Event Service URL

@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.json
    event_id = data.get("event_id")

    if not event_id:
        return jsonify({"error": "Event ID is required"}), 400

    # ✅ Use the correct Event Service URL (8080)
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

    return jsonify({"booking_id": new_booking.id, "status": "Pending"}), 201


# ✅ Move `if __name__ == "__main__":` to the end
if __name__ == "__main__":
    app.run(debug=True, port=5001)
