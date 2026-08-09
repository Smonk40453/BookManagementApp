import sqlite3 
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
connection.commit()
print("Books table created successfully!")
connection.close()
