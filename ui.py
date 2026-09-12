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
#delete books
def delete_book(book_id):
    response = requests.delete(
        f"http://127.0.0.1:5000/books/{book_id}")
    if response.status_code == 200:
        return "Book deleted successfully!"
    else:
        return f"Error deleting book: {response.text}"
#helper function so that user is not exposed to book_id
def get_book_choices():
    response = requests.get("http://127.0.0.1:5000/books")
    if response.status_code == 200:
        books = response.json()
        choices = []
        for books in books:
            book_id = books[0]
            title = books[1]
            choices.append((title,book_id))
        return choices
    return []
#Function to load selectec book
def load_book(book_id):
    response = requests.get("http://127.0.0.1:5000/books")
    if response.status_code == 200:
        books = response.json()
        for book in books:
            if book[0] ==book_id:
                return(
                    book[1], #title
                    book[2], #author
                    book[3], #reading status
                    str(book[4]) if book[4] is not None else "Not Rated",
                    book[5] #notes
                )
    return " ", " ", None, None, " "
    
with gr.Blocks(title = "Book Managment App") as app:
    gr.Markdown("Book Managment App")
    gr.Markdown("Keep track of your personal reading collection.")
    book_selector =gr.Dropdown(
        choices=get_book_choices(),
        label="Select a Book")
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
    book_selector.change(
        fn=load_book,
        inputs=[book_selector],
        outputs=[title, author, reading_status, rating, notes] )
    add_button = gr.Button("Add Book")
    message =gr.Textbox(label="Status", interactive=False)
    add_button.click(
        fn=add_book,
        inputs=[title, author, reading_status, rating, notes],
        outputs=message)
    update_button = gr.Button("Update Book")
    update_button.click(
        fn=update_book,
        inputs=[book_selector,title,author,reading_status,rating,notes],
        outputs=message)
    delete_button =gr.Button("Delete Book")
    delete_button.click(
        fn=delete_book,
        inputs=[book_selector],
        outputs=message)
    view_books_button = gr.Button("View Books")
    books_output = gr.JSON(label="My Books")
    view_books_button.click(
        fn=get_books,
        inputs=[],
        outputs=books_output)
app.launch()