import mysql.connector
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

# 1. Connect to the Cloud Database
print("🔌 Connecting to the database...")

if os.getenv('DB_URL'):
    # Parse the Render Database URL
    url = urlparse(os.getenv('DB_URL'))
    conn = mysql.connector.connect(
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path[1:],
        port=url.port,
        ssl_disabled=False
    )
else:
    # Fallback to manual variables if DB_URL is missing
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=3306
    )

cursor = conn.cursor()
print("✅ Connected!")

# ==========================================
# 2. CLEAN SLATE (Drop old tables to avoid duplicates)
# ==========================================
print("🗑️ Clearing old data...")
cursor.execute("DROP TABLE IF EXISTS testimonials")
cursor.execute("DROP TABLE IF EXISTS services")
cursor.execute("DROP TABLE IF EXISTS skills")
cursor.execute("DROP TABLE IF EXISTS projects")
cursor.execute("DROP TABLE IF EXISTS users") # Renamed from 'bio' to match your schema

# ==========================================
# 3. CREATE TABLES
# ==========================================
print("🏗️ Creating tables...")

# Users / Bio Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    role VARCHAR(255),
    intro TEXT,
    description TEXT,
    email VARCHAR(255),
    phone VARCHAR(255),
    linkedin VARCHAR(255),
    github VARCHAR(255),
    website VARCHAR(255)
)
''')

# Projects Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    technologies VARCHAR(255),
    link VARCHAR(255),
    image_url VARCHAR(255)
)
''')

# Skills Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
)
''')

# Services Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    icon VARCHAR(50)
)
''')

# Testimonials Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS testimonials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    role VARCHAR(255),
    content TEXT
)
''')

# ==========================================
# 4. INSERT REAL DATA
# ==========================================
print("💾 Inserting Real Data...")

# --- BIO ---
bio_sql = '''INSERT INTO users (name, role, intro, description, email, phone, linkedin, github, website) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
bio_val = (
    "Michael Owoeye",
    "Product Project Manager",
    "Strategic and user-centric Product Project Manager with over a decade of experience.",
    "My name is Michael Owoeye. I am a strategic and user-centric Product Project Manager with over a decade of experience leading digital product development projects from idea to launch. With a strong background in product design, project delivery, agile methodology, and cross-functional team leadership, I specialize in transforming business goals into intuitive digital solutions.",
    "owoeyemo@gmail.com",
    "+2348028753665",
    "https://linkedin.com/in/owoeyemichael",
    "https://github.com/owoeyemo",
    "https://www.owoeyemichael.com.ng"
)
cursor.execute(bio_sql, bio_val)

# --- SKILLS ---
skills_data = [
    ("Product Discovery & Strategy",),
    ("Agile & Scrum Methodologies",),
    ("Wireframing & Prototyping (Figma, Miro)",),
    ("Strategic Roadmapping & Prioritization",),
    ("User Research & Journey Mapping",),
    ("Data-Driven Decision Making",),
    ("Cross-Functional Team Leadership",),
    ("Product Analytics (Mixpanel, Google Analytics)",),
    ("Product Launch (Go-To-Market Strategy)",),
    ("PMO Leadership and Training",),
    ("Project Management Tools (Jira, Asana, Trello)",)
]
cursor.executemany("INSERT INTO skills (name) VALUES (%s)", skills_data)

# --- PROJECTS ---
projects_data = [
    ("Spectrum Aesthetics App", "A HIPAA-compliant client portal and mobile application designed for a cosmetic surgery practice, facilitating secure patient communication and scheduling.", "Mobile App, Healthcare Tech, HIPAA", "https://spectrumaesthetics.com", "https://via.placeholder.com/600x400?text=Spectrum"),
    ("Brandville Website", "A corporate website for Brandville Technologies, showcasing their expertise in designing and building digital experiences for diverse clients.", "Web Design, Corporate Branding, UI/UX", "https://brandville.com", "https://via.placeholder.com/600x400?text=Brandville"),
    ("Emmadunamix Web Portal", "A robust logistics web portal providing shipment tracking, fleet management, and secure operational workflows for China-to-Nigeria shipping.", "Logistics, Web Portal, Tracking Systems", "#", "https://via.placeholder.com/600x400?text=Emmadunamix"),
    ("PalliMoni", "A fintech mobile application focused on simplifying payments, savings, and financial transactions for underbanked users.", "Fintech, Mobile Payment, Secure Banking", "#", "https://via.placeholder.com/600x400?text=PalliMoni"),
    ("PrintStarz", "An on-demand online printing platform that allows users to design, order, and track custom print materials with ease.", "E-commerce, Custom Printing, Web App", "#", "https://via.placeholder.com/600x400?text=PrintStarz"),
    ("DelSprint Logistics", "A comprehensive logistics and delivery solution platform emphasizing speed, reliability, and safety for last-mile deliveries.", "Logistics, Delivery Tech, Operations", "#", "https://via.placeholder.com/600x400?text=DelSprint")
]
cursor.executemany("INSERT INTO projects (title, description, technologies, link, image_url) VALUES (%s, %s, %s, %s, %s)", projects_data)

# --- SERVICES ---
services_data = [
    ("Product Management", "End-to-end product leadership from strategy and roadmapping to execution and optimization.", "fa-rocket"),
    ("Training & Coaching", "Elevate your product teams with customized workshops, one-on-one mentorship, and hands-on training programs.", "fa-chalkboard-teacher"),
    ("Speaking Engagements", "Inspiring keynotes and interactive panels on product innovation, digital transformation, and the future of fintech.", "fa-microphone")
]
cursor.executemany("INSERT INTO services (title, description, icon) VALUES (%s, %s, %s)", services_data)

# --- TESTIMONIALS ---
testimonials_data = [
    ("Abigunde Emmanuel", "Event Director, Gineako", "Michael's strategic vision completely transformed our product roadmap. His ability to distill complex user needs into actionable features is exceptional."),
    ("Olukunle Oguniran", "CEO, Omnidunamis Web", "Working with Michael elevated our entire team. His coaching helped us adopt user-centric thinking and agile practices that doubled our velocity."),
    ("Victor Run", "VP Product, Spectrum Aesthetics App", "Michael's keynote was the highlight of our conference. His practical insights on scaling digital products sparked meaningful conversations.")
]
cursor.executemany("INSERT INTO testimonials (name, role, content) VALUES (%s, %s, %s)", testimonials_data)

# ==========================================
# 5. COMMIT AND CLOSE
# ==========================================
conn.commit()
cursor.close()
conn.close()

print("✅ SUCCESS! All Real Data (Bio, Skills, Projects, Services, Testimonials) has been added to the Cloud Database.")