import gradio as gr
import requests
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
with gr.Blocks(title = "Book Managment App") as app:
    gr.Markdown("Book Managment App")
    gr.Markdown("Keep track of your personal reading collection.")
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
app.launch()