import mysql.connector

# 1. Connect to Localhost (Your Laptop)
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='portfolio_db'
)
cursor = conn.cursor()

# 2. Delete the confused tables
print("💥 Deleting old tables...")
cursor.execute("DROP TABLE IF EXISTS bio")
cursor.execute("DROP TABLE IF EXISTS users")  # Delete the old 'users' table too

# 3. Create the CORRECT 'bio' table
print("🏗️ Creating new bio table...")
cursor.execute("""
CREATE TABLE bio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    intro_title VARCHAR(255),
    about_text TEXT,
    profile_image_url VARCHAR(255),
    resume_url VARCHAR(255),
    linkedin_url VARCHAR(255),
    twitter_url VARCHAR(255),
    github_url VARCHAR(255),
    email_contact VARCHAR(255)
)
""")

# 4. Add the data
print("📝 Adding data...")
cursor.execute("""
INSERT INTO bio (intro_title, about_text, email_contact, profile_image_url, resume_url, linkedin_url, twitter_url, github_url) 
VALUES (
    'Product Manager', 
    'I build amazing products...', 
    'michael@example.com', 
    'https://placehold.co/400', 
    '#',
    '#',
    '#',
    '#'
)
""")

conn.commit()
conn.close()
print("✅ SUCCESS! Database Fixed.")