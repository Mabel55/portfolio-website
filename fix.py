import os
import mysql.connector
from dotenv import load_dotenv

# 1. Point directly to the .env file in the backend folder
env_path = os.path.join('backend', '.env')
load_dotenv(env_path)

try:
    # 2. Connect to the database
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT')) if os.getenv('DB_PORT') else 11988
    )
    cursor = conn.cursor()
    print("✅ Successfully connected to the database!")

    # 3. Create the missing icon_url column
    try:
        cursor.execute("ALTER TABLE services ADD COLUMN icon_url VARCHAR(255)")
        print("✅ Created the missing 'icon_url' column.")
    except mysql.connector.Error as err:
        if err.errno == 1060: # Column already exists
            print("ℹ️ Column 'icon_url' already exists. Skipping...")
        else:
            print(f"❌ Error creating column: {err}")

    # 4. Update with the high-quality Figma links
    updates = [
        ("https://raw.githubusercontent.com/Mabel55/portfolio-website/main/backend/images/rocket.svg", "Product Management"),
        ("https://raw.githubusercontent.com/Mabel55/portfolio-website/main/backend/images/training.svg", "Training & Coaching"),
        ("https://raw.githubusercontent.com/Mabel55/portfolio-website/main/backend/images/speaking.svg", "Speaking Engagements")
    ]

    for url, title in updates:
        sql = "UPDATE services SET icon_url = %s WHERE title LIKE %s"
        cursor.execute(sql, (url, f"%{title}%"))

    conn.commit()
    print("🎉 FINAL SUCCESS! Your icons are now live and high-quality.")

except Exception as e:
    print(f"❌ Connection Error: {e}")
    print("TIP: Check if your .env file is inside the 'backend' folder.")

finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()