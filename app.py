from flask import Flask, jsonify,request
import sqlite3

app = Flask(__name__)
@app.route("/")
def home():
    return "Book Management App is running!"
@app.route("/books", methods=["GET"])
def get_books():
    connection = sqlite3.connect("book_managment.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    connection.close()
    return jsonify(books)
@app.route("/books",methods=["POST"])
def add_book():
    data = request.get_json()
    title = data.get("title")
    author = data.get("author")
    reading_status = data.get("reading_status")
    rating = data.get("rating")
    notes = data.get("notes")
    if not title or not author or not reading_status:
        return jsonify({"error": "Title, author, and reading status are required."}), 400
    connection = sqlite3.connect("book_managment.db")
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO books (title, author, reading_status, rating, notes)
        VALUES (?,?,?,?,?)
    """,(title, author, reading_status, rating, notes))
    connection.commit()
    book_id = cursor.lastrowid
    connection.close()
    return jsonify({
        "message": "Book added successfully!",
        "book_id": book_id 
    }), 201    
@app.route ("/books/<int:book_id>",methods=["PUT"])
def update_book(book_id):
    data=request.get_json()
    title = data.get("title")
    author = data.get("author")
    reading_status = data.get("reading_status")
    rating = data.get("rating")
    notes  = data.get("notes")
    if not title or not author or not reading_status:
        return jsonify({"error": "Title, author, and reading status are required."}), 400 
    connection = sqlite3.connect("book_managment.db")
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE books
        SET title = ?, author = ?, reading_status = ?, rating = ?, notes = ?
        WHERE book_id = ?
    """,(
        title, 
        author, 
        reading_status,
        rating, 
        notes,
        book_id
    ))
    connection.commit()
    if cursor.rowcount == 0:
        connection.close()
        return jsonify({"error": "Book note found."}),404
    connection.close()
    return jsonify({
        "message": "Book updated successfully!"}),200
