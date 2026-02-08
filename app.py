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

@app.route('/api/bio', methods=['GET'])
def get_bio():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # ✅ CORRECTED: We select from 'users', not 'bio'
        cursor.execute("SELECT * FROM users LIMIT 1")
        bio = cursor.fetchone()
        
        conn.close()
        
        if bio:
            return jsonify(bio)
        else:
            return jsonify({"error": "No user data found"}), 404

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

# ========================================================
# 🛠️ SECRET SETUP ROUTE (Paste this at the bottom of app.py)
# ========================================================
@app.route('/setup-data')
def setup_data():
    try:
        # 1. Connect to Database
        if os.getenv('DB_URL'):
            import urllib.parse
            url = urllib.parse.urlparse(os.getenv('DB_URL'))
            conn = mysql.connector.connect(
                host=url.hostname, user=url.username, password=url.password,
                database=url.path[1:], port=url.port
            )
        else:
            conn = mysql.connector.connect(
                host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'), database=os.getenv('DB_NAME'),
                port=3306
            )
        
        cursor = conn.cursor()

        # 2. DROP TABLES (Clean Slate)
        cursor.execute("DROP TABLE IF EXISTS testimonials")
        cursor.execute("DROP TABLE IF EXISTS services")
        cursor.execute("DROP TABLE IF EXISTS skills")
        cursor.execute("DROP TABLE IF EXISTS projects")
        cursor.execute("DROP TABLE IF EXISTS users")

        # 3. CREATE TABLES
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), role VARCHAR(255), intro TEXT, description TEXT, email VARCHAR(255), phone VARCHAR(255), linkedin VARCHAR(255), github VARCHAR(255), website VARCHAR(255))")
        cursor.execute("CREATE TABLE IF NOT EXISTS projects (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), description TEXT, technologies VARCHAR(255), link VARCHAR(255), image_url VARCHAR(255))")
        cursor.execute("CREATE TABLE IF NOT EXISTS skills (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
        cursor.execute("CREATE TABLE IF NOT EXISTS services (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), description TEXT, icon VARCHAR(50))")
        cursor.execute("CREATE TABLE IF NOT EXISTS testimonials (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), role VARCHAR(255), content TEXT)")

        # 4. INSERT REAL DATA
        # --- Bio ---
        bio_val = ("Michael Owoeye", "Product Project Manager", "Strategic and user-centric Product Project Manager with over a decade of experience.", "My name is Michael Owoeye. I am a strategic and user-centric Product Project Manager with over a decade of experience leading digital product development projects from idea to launch. With a strong background in product design, project delivery, agile methodology, and cross-functional team leadership, I specialize in transforming business goals into intuitive digital solutions.", "owoeyemo@gmail.com", "+2348028753665", "https://linkedin.com/in/owoeyemichael", "https://github.com/owoeyemo", "https://www.owoeyemichael.com.ng")
        cursor.execute("INSERT INTO users (name, role, intro, description, email, phone, linkedin, github, website) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", bio_val)

        # --- Skills ---
        skills = [("Product Discovery & Strategy",), ("Agile & Scrum Methodologies",), ("Wireframing & Prototyping (Figma, Miro)",), ("Strategic Roadmapping",), ("User Research",), ("Data-Driven Decision Making",), ("Cross-Functional Team Leadership",), ("Product Analytics (Mixpanel, GA)",), ("Go-To-Market Strategy",), ("PMO Leadership",), ("Jira, Asana, Trello",)]
        cursor.executemany("INSERT INTO skills (name) VALUES (%s)", skills)

        # --- Projects ---
        projects = [
            ("Spectrum Aesthetics App", "A HIPAA-compliant client portal and mobile application designed for a cosmetic surgery practice.", "Mobile App, Healthcare Tech, HIPAA", "https://spectrumaesthetics.com", "https://via.placeholder.com/600x400?text=Spectrum"),
            ("Brandville Website", "A corporate website for Brandville Technologies, showcasing their expertise in digital experiences.", "Web Design, Corporate Branding", "https://brandville.com", "https://via.placeholder.com/600x400?text=Brandville"),
            ("Emmadunamix Web Portal", "A robust logistics web portal providing shipment tracking, fleet management, and operational workflows.", "Logistics, Web Portal, Tracking", "#", "https://via.placeholder.com/600x400?text=Emmadunamix"),
            ("PalliMoni", "A fintech mobile application focused on simplifying payments, savings, and financial transactions.", "Fintech, Mobile Payment", "#", "https://via.placeholder.com/600x400?text=PalliMoni"),
            ("PrintStarz", "An on-demand online printing platform that allows users to design, order, and track custom prints.", "E-commerce, Custom Printing", "#", "https://via.placeholder.com/600x400?text=PrintStarz"),
            ("DelSprint Logistics", "A comprehensive logistics and delivery solution platform emphasizing speed and reliability.", "Logistics, Delivery Tech", "#", "https://via.placeholder.com/600x400?text=DelSprint")
        ]
        cursor.executemany("INSERT INTO projects (title, description, technologies, link, image_url) VALUES (%s, %s, %s, %s, %s)", projects)

        # --- Services ---
        services = [
            ("Product Management", "End-to-end product leadership from strategy and roadmapping to execution and optimization.", "fa-rocket"),
            ("Training & Coaching", "Elevate your product teams with customized workshops, one-on-one mentorship, and hands-on training programs.", "fa-chalkboard-teacher"),
            ("Speaking Engagements", "Inspiring keynotes and interactive panels on product innovation, digital transformation, and the future of fintech.", "fa-microphone")
        ]
        cursor.executemany("INSERT INTO services (title, description, icon) VALUES (%s, %s, %s)", services)

        # --- Testimonials ---
        testimonials = [
            ("Abigunde Emmanuel", "Event Director, Gineako", "Michael's strategic vision completely transformed our product roadmap. His ability to distill complex user needs into actionable features is exceptional."),
            ("Olukunle Oguniran", "CEO, Omnidunamis Web", "Working with Michael elevated our entire team. His coaching helped us adopt user-centric thinking and agile practices that doubled our velocity."),
            ("Victor Run", "VP Product, Spectrum Aesthetics App", "Michael's keynote was the highlight of our conference. His practical insights on scaling digital products sparked meaningful conversations.")
        ]
        cursor.executemany("INSERT INTO testimonials (name, role, content) VALUES (%s, %s, %s)", testimonials)

        conn.commit()
        conn.close()
        return "✅ SUCCESS! Database Reset and Populated with REAL DATA!"
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
    
