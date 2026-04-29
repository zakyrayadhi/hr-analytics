import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="postgres",  # connect to default DB
    user="postgres",
    password="admin"
)

conn.autocommit = True
cursor = conn.cursor()

cursor.execute("CREATE DATABASE hr_warehouse;")

cursor.close()
conn.close()

print("✅ Database created")