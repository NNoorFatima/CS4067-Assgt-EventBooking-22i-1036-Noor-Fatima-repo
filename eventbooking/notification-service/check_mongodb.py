from pymongo import MongoClient

# MongoDB Atlas Connection
MONGO_URI = "mongodb+srv://Event-Service:123@cluster0.ieune.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["notification_service"]
notifications_collection = db["notifications"]

# Check stored notifications
notifications = list(notifications_collection.find({}))

print("\n✅ Stored Notifications in MongoDB:")
for notif in notifications:
    print(notif)

if not notifications:
    print("❌ No notifications found in MongoDB.")
