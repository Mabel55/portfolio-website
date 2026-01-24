import mysql.connector
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

# 1. Connect to the Cloud (Using the logic that JUST worked)
if os.getenv('DB_URL'):
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
    # Fallback to manual if DB_URL is missing
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database='defaultdb',
        port=11988,
        ssl_disabled=False
    )

cursor = conn.cursor()

# 2. Create the "Users" table (For /api/bio)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    role VARCHAR(255),
    bio TEXT,
    image_url VARCHAR(255)
)
''')

# 3. Create the other tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    link VARCHAR(255)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    level VARCHAR(50)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    message TEXT
)
''')

# 4. Insert dummy data so the error goes away immediately
cursor.execute('SELECT * FROM users WHERE id = 1')
if not cursor.fetchone():
    cursor.execute('''
        INSERT INTO users (name, role, bio, image_url) 
        VALUES ('Mabel', 'Developer', 'I am a backend developer!', 'https://via.placeholder.com/150')
    ''')
    print("Added dummy user!")

conn.commit()
print("SUCCESS: All tables created in the Cloud!")
conn.close()