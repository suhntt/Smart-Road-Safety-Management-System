from utils.db import get_db_connection

conn = get_db_connection()
print("✅ Connected to MySQL successfully!")

conn.close()
