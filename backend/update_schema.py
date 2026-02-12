import mysql.connector

# 1. Connect to CLOUD DATABASE
# (Copy your details from Render Environment)
conn = mysql.connector.connect(
    host='mysql-1de56a9b-nasaadanna-6430.j.aivencloud.com',
    port=11988,
    user='avnadmin',
    password='HIDDEN_PASSWORD',
    database='defaultdb',
    ssl_disabled=True
)
cursor = conn.cursor()

print("⚙️  Upgrading Database Schema...")

# --- TASK 1: Upgrade BIO Table (Add Stats & Resume) ---
# We use 'try/except' in case you run this twice (avoids crashing)
try:
    cursor.execute("ALTER TABLE bio ADD COLUMN resume_url VARCHAR(255)")
    print("✅ Added 'resume_url' to bio.")
except:
    print("ℹ️  'resume_url' already exists.")

try:
    cursor.execute("ALTER TABLE bio ADD COLUMN stat_years VARCHAR(50)")
    cursor.execute("ALTER TABLE bio ADD COLUMN stat_products VARCHAR(50)")
    cursor.execute("ALTER TABLE bio ADD COLUMN stat_users VARCHAR(50)")
    print("✅ Added Stats columns to bio.")
except:
    print("ℹ️  Stats columns already exist.")

# --- TASK 2: Create SERVICES Table (New) ---
cursor.execute("DROP TABLE IF EXISTS services")
cursor.execute("""
CREATE TABLE services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    icon_url VARCHAR(255)
)
""")
print("✅ Created 'services' table.")

# --- TASK 3: Add Dummy Data for Services ---
cursor.execute("""
INSERT INTO services (title, description, icon_url) 
VALUES 
    ('Product Management', 'I help organizations transform complex challenges into elegant solutions.', 'https://placehold.co/50'),
    ('Training & Coaching', 'I mentor product teams with customized workshops.', 'https://placehold.co/50'),
    ('Speaking Engagements', 'Inspiring keynotes on the future of product innovation.', 'https://placehold.co/50')
""")
print("📝 Added dummy services data.")

conn.commit()
conn.close()
print("🚀 Database Upgrade Complete!")