#  User Service Microservice

##  Overview
The **User Service** is a microservice built with **FastAPI** and **PostgreSQL** to handle user authentication and management for the Online Event Booking Platform. It provides **user registration, login, and authentication** using JWT (JSON Web Token) security.

---

##  Project Structure
```
user-service/
│── app/
│   │── database.py        # Database connection setup
│   │── models.py          # SQLAlchemy User model
│   │── auth.py            # Password hashing & JWT token functions
│   │── routes/
│   │   ├── user_routes.py # API routes for registration & login
│   │── main.py            # FastAPI app entry point
│── .env                   # Environment variables
│── requirements.txt        # Dependencies
│── README.md               # Documentation
```

---

##  Installation & Setup
###  Clone the Repository
```bash
git clone https://github.com/your-repo/eventbooking-user-service.git
cd eventbooking-user-service
```

###  Create & Activate Virtual Environment
```bash
python -m venv venv
# Activate on Windows
venv\Scripts\activate
# Activate on macOS/Linux
source venv/bin/activate
```


###  Install Dependencies
```bash
pip install -r requirements.txt
```

###  Configure Environment Variables
Create a `.env` file in the root directory:
```
DATABASE_URL=postgresql://username:password@localhost:5432/user_service_db
SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

##  Running the Service
###  Start FastAPI Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

###  Access API Docs
Once the server is running, open the following URL:
```
http://127.0.0.1:8000/docs
```
This provides an interactive **Swagger UI** for testing API endpoints.

---

##  API Endpoints
### **User Registration**
**Endpoint:** `POST /users/register`
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword"
}
```
 **Response:** `{ "message": "User registered successfully" }`

### **User Login**
**Endpoint:** `POST /users/login`
```json
{
    "username": "john_doe",
    "password": "securepassword"
}
```
 **Response:** `{ "access_token": "<jwt_token>", "token_type": "bearer" }`

### **Get Current User (Protected Route)**
**Endpoint:** `GET /users/me`
**Headers:** `Authorization: Bearer <jwt_token>`

---

##  Security Features
- **Password Hashing:** Uses bcrypt to securely hash passwords before storing them.
- **JWT Authentication:** Generates a token on successful login for secure API access.
- **CORS Enabled:** Allows frontend apps to communicate with the backend.

---

##  Future Improvements
-  **Integration with Event & Booking Services**
-  **Email verification on user registration**
-  **OAuth2.0 / Google Login Support**

---

##  Troubleshooting
###  Database Connection Issues
If the database connection fails, ensure that PostgreSQL is running and the `.env` variables are correct:
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/user_service_db
```

###  JWT Authentication Not Working?
Ensure the **SECRET_KEY** in `.env` is correctly set and used consistently across authentication functions.

###  Server Not Starting?
Check for errors in **FastAPI logs** and confirm dependencies are installed:
```bash
pip install -r requirements.txt
```

---

##  Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m "Added new feature"`)
4. Push to your branch (`git push origin feature-branch`)
5. Create a Pull Request 🚀

---



---


