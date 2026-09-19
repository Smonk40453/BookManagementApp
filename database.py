import sqlite3 
from werkzeug.security import generate_password_hash
connection = sqlite3.connect("book_management.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
               book_id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT NOT NULL,
               author TEXT NOT NULL,
               reading_status TEXT NOT NULL,
               rating INTEGER,
               notes TEXT
    )
""")
cursor.execute("""
               CREATE TABLE IF NOT EXISTS users (
               user_id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL UNIQUE,
               password_hash TEXT NOT NULL
               )
               """)
password_hash = generate_password_hash("BookTracker123!")
cursor.execute("""
               INSERT OR IGNORE INTO users (username, password_hash)
               VALUES (?, ?)
               """, ("admin", password_hash))
connection.commit()
print("Books table created successfully!")
connection.close()
