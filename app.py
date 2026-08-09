from flask import Flask, jsonify
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