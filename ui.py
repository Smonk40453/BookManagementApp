import gradio as gr
import requests
#Add books to the library
def add_book(title, author,reading_status,rating,notes):
    if rating =="Not Rated":
        rating = None
    else:
        rating = int(rating)
    book_data ={
        "title": title,
        "author": author,
        "reading_status": reading_status,
        "rating": rating,
        "notes": notes}
    response =requests.post(
        "http://127.0.0.1:5000/books",
        json=book_data)
    if response.status_code == 201:
        return "Book added successfully!"
    return f"Error adding book: {response.text}"
#Grab books from the database 
def get_books():
    response = requests.get("http://127.0.0.1:5000/books")
    if response.status_code == 200:
        books = response.json()
        return books
    else:
        return "Unable to retrieve books."
#Update books
def update_book(book_id, title, author,reading_status,rating,notes):
    book_data = {
        "title":title,
        "author":author,
        "reading_status":reading_status,
        "rating": rating,
        "notes":notes}
    response = requests.put(
        f"http://127.0.0.1:5000/books/{book_id}",
        json=book_data)
    if response.status_code == 200:
        return "Book updated successfully!"
    else:
        return f"Error updating book: {response.text}"
    
with gr.Blocks(title = "Book Managment App") as app:
    gr.Markdown("Book Managment App")
    gr.Markdown("Keep track of your personal reading collection.")
    book_id = gr.Number(label="Book ID", precision=0)
    title = gr.Textbox(label ="Book Title")
    author = gr.Textbox(label= "Author")
    reading_status = gr.Dropdown(
        choices=[
            "Want to Read",
            "Currently Reading",
            "Completed",
            "Did Not Finish"
        ],
        label="Reading Status")
    rating =gr.Dropdown(
        choices=["Not Rated","1","2","3","4","5"],
        label="Rating")
    notes = gr.Textbox(
        label="Personal Notes",
        lines=4)
    add_button = gr.Button("Add Book")
    message =gr.Textbox(label="Status", interactive=False)
    add_button.click(
        fn=add_book,
        inputs=[title, author, reading_status, rating, notes],
        outputs=message)
    update_button = gr.Button("Update Book")
    update_button.click(
        fn=update_book,
        inputs=[book_id,title,author,reading_status,rating,notes],
        outputs=message)
    view_books_button = gr.Button("View Books")
    books_output = gr.JSON(label="My Books")
    view_books_button.click(
        fn=get_books,
        inputs=[],
        outputs=books_output)
app.launch()