from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import mysql.connector
from datetime import timedelta
import os

# ---------------------- Flask Setup ----------------------
app = Flask(__name__)
CORS(app)

# Secret Key for JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with your own
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

# ---------------------- Database Connection ----------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # change to your MySQL user
        password="",  # change to your MySQL password
        database="delivery_system"  # change to your DB name
    )

# ---------------------- User Auth APIs ----------------------

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    role = data['role']  # 'admin', 'producer', 'consumer', 'dispatcher'

    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                       (name, email, password, role))
        db.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user:
        token = create_access_token(identity={"id": user["id"], "role": user["role"], "name": user["name"]})
        return jsonify({"token": token, "user": user}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# ---------------------- Protected Endpoint Example ----------------------

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({"message": "Access granted!", "user": current_user})

# ---------------------- Health Check ----------------------

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "API is running"}), 200

# ---------------------- Run Flask App ----------------------

if __name__ == '__main__':
    app.run(debug=True)
