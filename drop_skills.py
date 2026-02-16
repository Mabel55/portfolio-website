import os
import mysql.connector
from dotenv import load_dotenv

# Find the password in the backend folder
load_dotenv(os.path.join('backend', '.env'))

# Connect to the database
conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    port=int(os.getenv('DB_PORT'))
)
cursor = conn.cursor()

# 🚨 THE CLEANUP COMMAND: Delete only the skills table
cursor.execute("DROP TABLE IF EXISTS skills")

conn.commit()
print("✅ Success! The 'skills' table has been completely removed from the database.")

conn.close()