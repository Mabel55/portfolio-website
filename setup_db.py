import os
import mysql.connector
from flask import Flask, jsonify, request # <--- Added request here
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host='mysql-1de56a9b-nasaadanna-6430.j.aivencloud.com',
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database='defaultdb',
        port=11988,
        ssl_disabled=False
    )

# 1. BIO (GET)
@app.route('/api/bio')
def get_bio():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE id = 1')
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(data) if data else (jsonify({"error": "No bio found"}), 404)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. PROJECTS (GET)
@app.route('/api/projects')
def get_projects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM projects')
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. SKILLS (GET)
@app.route('/api/skills')
def get_skills():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM skills')
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. CONTACT FORM (POST)
@app.route('/api/contact', methods=['POST'])
def contact_form():
    try:
        data = request.json # Get the data sent from Frontend
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Save the message to the database
        query = "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, message))
        
        conn.commit() # Save changes
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Message sent successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)