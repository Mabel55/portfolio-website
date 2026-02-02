from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT')),
        ssl_disabled=True
    )

# --- 1. BIO ENDPOINT (Updated to include Resume & Stats automatically) ---
@app.route('/api/bio', methods=['GET'])
def get_bio():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # SELECT * will automatically pick up the new 'resume_url' and 'stat_years' columns!
        cursor.execute("SELECT * FROM bio LIMIT 1")
        bio = cursor.fetchone()
        conn.close()
        return jsonify(bio)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 2. PROJECTS ENDPOINT ---
@app.route('/api/projects', methods=['GET'])
def get_projects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM projects")
        projects = cursor.fetchall()
        conn.close()
        return jsonify(projects)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 3. SKILLS ENDPOINT ---
@app.route('/api/skills', methods=['GET'])
def get_skills():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM skills")
        skills = cursor.fetchall()
        conn.close()
        return jsonify(skills)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 4. SERVICES ENDPOINT (!!! NEW !!!) ---
@app.route('/api/services', methods=['GET'])
def get_services():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM services")
        services = cursor.fetchall()
        conn.close()
        return jsonify(services)
    except Exception as e:
        # If the table doesn't exist yet, return an empty list instead of crashing
        return jsonify([]), 200 

# --- 5. TESTIMONIALS ENDPOINT ---
@app.route('/api/testimonials', methods=['GET'])
def get_testimonials():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM testimonials")
        testimonials = cursor.fetchall()
        conn.close()
        return jsonify(testimonials)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 6. CONTACT ENDPOINT ---
@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    # In a real app, you would save this to DB or send an email here
    return jsonify({"message": "Message received!", "data": data}), 201

if __name__ == '__main__':
    app.run(debug=True)