from flask import Flask, jsonify,request,session
import sqlite3
from werkzeug.security import check_password_hash
app = Flask(__name__)
app.secret_key = "book-tracker-secret-key"
@app.route("/")
def home():
    return "Book Management App is running!"
@app.route("/login", methods=["POST"])
def login():
    data=request.get_json()
    username =data.get("username")
    password=data.get("password")
    connection = sqlite3.connect("book_management.db")
    cursor=connection.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user=cursor.fetchone()
    connection.close()
    if user and check_password_hash(user[2], password):
        session["user_id"] = user[0]
        session["username" ]= user[1]
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid username or password."}), 401
@app.route("/logout",methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logout successful!"}), 200       
@app.route("/books", methods=["GET"])
def get_books():
    if "user_id" not in session:
        return jsonify({"message": "Unauthorized. Please log in."}), 401
    connection = sqlite3.connect("book_management.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    connection.close()
    return jsonify(books)
@app.route("/books",methods=["POST"])
def add_book():
    if "user_id" not in session:
        return jsonify({"message": "Unauthorized. Please log in."}), 401
    data = request.get_json()
    title = data.get("title")
    author = data.get("author")
    reading_status = data.get("reading_status")
    rating = data.get("rating")
    notes = data.get("notes")
    if not title or not author or not reading_status:
        return jsonify({"error": "Title, author, and reading status are required."}), 400
    connection = sqlite3.connect("book_management.db")
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
    if "user_id" not in session:
        return jsonify({"message": "Unauthorized. Please log in."}), 401
    data=request.get_json()
    title = data.get("title")
    author = data.get("author")
    reading_status = data.get("reading_status")
    rating = data.get("rating")
    notes  = data.get("notes")
    if not title or not author or not reading_status:
        return jsonify({"error": "Title, author, and reading status are required."}), 400 
    connection = sqlite3.connect("book_management.db")
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
        return jsonify({"error": "Book not found."}),404
    connection.close()
    return jsonify({
        "message": "Book updated successfully!"}),200
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    if "user_id" not in session:
        return jsonify({"message": "Unauthorized. Please log in."}), 401
    connection = sqlite3.connect("book_management.db")
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM books WHERE book_id = ?",
        (book_id,)
    )
    connection.commit()
    if cursor.rowcount == 0:
        connection.close()
        return jsonify({"error": "Book note found."}),404
    connection.close()
    return jsonify({
        "message":"Book deleted successfully!"}),200
    
