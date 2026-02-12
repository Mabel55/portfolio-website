import mysql.connector

# 1. Connect to YOUR CLOUD DATABASE (Aiven)
# REPLACE THESE VALUES with what is in your Render Environment!
conn = mysql.connector.connect(
    host='mysql-1de56a9b-nasaadanna-6430.j.aivencloud.com',           
    port=11988,                            
    user='avnadmin',                       
    password='HIDDEN_PASSWORD',   
    database='defaultdb',
    ssl_disabled=True
)
cursor = conn.cursor()

# 2. Create the Testimonials Table
print("🔨 Building Testimonials table in Cloud...")
cursor.execute("DROP TABLE IF EXISTS testimonials")

cursor.execute("""
CREATE TABLE testimonials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_name VARCHAR(255),
    client_role VARCHAR(255),
    content TEXT,
    client_photo_url VARCHAR(255)
)
""")

# 3. Add Dummy Data
print("📝 Adding sample testimonials...")
cursor.execute("""
INSERT INTO testimonials (client_name, client_role, content, client_photo_url) 
VALUES 
    ('Sarah Johnson', 'CEO at TechStart', 'Mabel is an incredible backend engineer. The API is fast and reliable!', 'https://placehold.co/100'),
    ('David Lee', 'Product Manager', 'Great communication and perfect code quality.', 'https://placehold.co/100')
""")

conn.commit()
conn.close()
print("✅ FIXED! Testimonials table created in Cloud.")