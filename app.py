from flask import Flask, jsonify, request
from urllib.parse import urlparse
import mysql.connector
import os 
app = Flask(__name__)

# Database Configuration
if os.getenv('DB_URL'):
    # We are on the Cloud (Render) - Parse the long URL
    url = urlparse(os.getenv('DB_URL'))
    db_config = {
        'host': url.hostname,
        'user': url.username,
        'password': url.password,
        'database': url.path[1:],  # Removes the leading '/'
        'port': url.port
    }
else:
    # We are on the Laptop (Localhost)
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '1234',  # Or whatever your local password is
        'database': 'portfolio_db'
    }
# Helper function to get a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)


# BIO  First API Endpoint!

@app.route('/api/bio', methods=['GET'])
def get_bio():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # dictionary=True makes data look like JSON
    
    cursor.execute("SELECT * FROM bio")
    bio_data = cursor.fetchone()          # We only expect 1 bio
    
    cursor.close()
    conn.close()
    
    
    return jsonify(bio_data)


# GET SKILLS

@app.route('/api/skills', methods=['GET'])
def get_skills():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM skills")
    skills_data = cursor.fetchall()       # We expect MANY skills
    
    cursor.close()
    conn.close()
    
    return jsonify(skills_data)



# GET PROJECTS 

@app.route('/api/projects', methods=['GET'])
def get_projects():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # show the newest projects first (ORDER BY id DESC)
    cursor.execute("SELECT * FROM projects ORDER BY id DESC")
    projects_data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(projects_data)


# SUBMIT CONTACT (Receiving Data)

from flask import request  

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.get_json()  # This grabs the JSON sent by the Frontend
    
    name = data.get('sender_name')
    email = data.get('sender_email')
    message = data.get('message_body')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO messages (sender_name, sender_email, message_body) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, message))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Email sent successfully!", "status": "success"}), 201

if __name__ == '__main__':
    app.run(debug=True)