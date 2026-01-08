import sqlite3

conn = sqlite3.connect("Food.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    price INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cart (
    user_id TEXT,
    food TEXT,
    quantity INTEGER,
    price INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    total INTEGER,
    payment_method TEXT,
    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    order_id INTEGER,
    food TEXT,
    quantity INTEGER,
    price INTEGER
)
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully")
