import mysql.connector

# CONNECT
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',  
    database='portfolio_db'
)
cursor = conn.cursor()

print("Connected! Fixing the database...")

# 1. Force the Update
cursor.execute("UPDATE projects SET category = 'Python' WHERE id > 0")
conn.commit() # <--- This saves it permanently

print("SUCCESS! Category updated to 'Python'.")

cursor.close()
conn.close()