import gradio as gr
import requests
api_session=requests.Session()
def login_user(username, password):
    response =api_session.post(
        "http://127.0.0.1:5000/login",
        json={
            "username": username,
            "password": password
        } 
    )
    if response.status_code == 200:
        return ("Login successful!",
                get_books(),
                gr.update(choices=get_book_choices())
        )
    else:
        return (
         "Invalid username or password.", 
         [],
         gr.update()
        )
def logout_user():
    response = api_session.post(
        "http://127.0.0.1:5000/logout")
    if response.status_code == 200:
        return ( 
            "Logout successful!",
            [],
            gr.update(choices=[], value=None)
        )
    else:
        return(
            "Error logging out",
            gr.update(),
            gr.update()
        )
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
    response = api_session.post(
        "http://127.0.0.1:5000/books",
        json=book_data)
    if response.status_code == 201:
        return "Book added successfully!", gr.update(choices=get_book_choices()),get_books()
    return f"Error adding book: {response.text}",gr.update(),gr.update()
#Grab books from the database 
def get_books():
    response = api_session.get("http://127.0.0.1:5000/books")
    if response.status_code == 200:
        books = response.json()
        library =[]
        for book in books:
            library.append([
                book[1], #title
                book[2], #author
                book[3], #status
                book[4] if book[4] is not None else "Not Rated",
                book[5] # notes
            ])
        return library
    else:
        return[]
#Update books
def update_book(book_id, title, author,reading_status,rating,notes):
    book_data = {
        "title":title,
        "author":author,
        "reading_status":reading_status,
        "rating": rating,
        "notes":notes}
    response = api_session.put(
        f"http://127.0.0.1:5000/books/{book_id}",
        json=book_data)
    if response.status_code == 200:
        return "Book updated successfully!",get_books()
    else:
        return f"Error updating book: {response.text}",gr.update()
#delete books
def delete_book(book_id):
    response = api_session.delete(
        f"http://127.0.0.1:5000/books/{book_id}")
    if response.status_code == 200:
        return ("Book deleted successfully!",gr.update(
            choices=get_book_choices(),
            value=None), get_books())
    else:
        return (f"Error deleting book: {response.text}", gr.update(),gr.update())
#helper function so that user is not exposed to book_id
def get_book_choices():
    response = api_session.get("http://127.0.0.1:5000/books")
    if response.status_code == 200:
        books = response.json()
        choices = []
        for books in books:
            book_id = books[0]
            title = books[1]
            choices.append((title,book_id))
        return choices
    return []
#Function to load selected book
def load_book(book_id):
    response = api_session.get("http://127.0.0.1:5000/books")
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
#Autorefresh when book is added
def refresh_book_selector():
    return gr.update(choices=get_book_choices())

theme = gr.themes.ThemeClass.from_hub("kbray/NeoSand")
theme.body_background_fill = "#F7F3EA"
theme.background_fill_primary ="#DDE5D5"
theme.block_background_fill ="#DDE5D5"
theme.input_background_fill ="#E8CFCE"
theme.button_primary_background_fill = "#A8B89A"
theme.buton_secondary_background_fill = "#E8CFCE"
theme.button_cancel_background_fill = "#D8A7A7"
theme.block_shadow ="0 4px 12px rgba(120, 130, 110, 0.18)"
theme.input_shadow="0 2px 6px rgba(120, 130, 110, 0.15)"
theme.table_even_background_fill = "#DDE5D5"
theme.table_odd_background_fill = "#E8CFCE"
theme.table_row_focus = "#F7F3EA"
theme.body_text_size = "16px"
with gr.Blocks(title = "Book Managment App", theme=theme) as app:
    gr.Markdown("# Book Managment App")
    gr.Markdown("### Keep track of your personal reading collection." )   
    with gr.Tabs():
        with gr.Tab("Login"):
            gr.Markdown("### Login to your Book Tracker")
            username_input = gr.Textbox(
                label="Username")
            password_input = gr.Textbox(
                label="Password",
                type="password")
            login_button = gr.Button(
                "Login",
                variant="primary")
            logout_button = gr.Button(
                "Logout",
                variant="stop")
            login_message = gr.Textbox(
                label="Status",
                interactive=False)
        with gr.Tab("My Library"):
            gr.Markdown( "### My Books")
            books_output = gr.Dataframe(
                headers=["Title", "Author", "Status", "Rating", "Notes"],
                interactive=False,
                label= "### My Books")
        with gr.Tab("Add Book"):
            with gr.Row():
                title = gr.Textbox(label ="Book Title")
                author = gr.Textbox(label= "Author")
            with gr.Row():
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
            add_button = gr.Button("Add Book", variant="primary")
            message =gr.Textbox(label="Status", interactive=False)
        with gr.Tab("Manage Books"):
             book_selector =gr.Dropdown(
                choices=get_book_choices(),
                label="Select a Book")
             with gr.Row():
                edit_title = gr.Textbox(label="Book title")
                edit_author = gr.Textbox(label="Author")
             with gr.Row():
                edit_reading_status = gr.Dropdown(
                 choices=["Want to Read","Reading","Completed"],
                 label="Reading Status")
                edit_rating = gr.Dropdown(
                 choices=["Not Rated","1","2","3","4","5"],
                 label="Rating")
             edit_notes = gr.Textbox(
                 label="Personal Notes",
                 lines=4)
             with gr.Row():
                update_button = gr.Button("Update Book", variant="primary")
                delete_button =gr.Button("Delete Book", variant="stop")
             manage_message = gr.Textbox(
                 label="Status",
                 interactive=False)
    book_selector.change(
        fn=load_book,
        inputs=[book_selector],
        outputs=[edit_title, edit_author, edit_reading_status, edit_rating, edit_notes] )
    app.load(
        fn=get_books,
        inputs=[],
        outputs=books_output)
    add_button.click(
                fn=add_book,
                inputs=[title, author, reading_status, rating, notes],
                outputs=[message, book_selector,books_output])
    
    update_button.click(
                fn=update_book,
                inputs=[book_selector,edit_title,edit_author,edit_reading_status,edit_rating,edit_notes],
                outputs=[manage_message, books_output])
    delete_button.click(
                fn=delete_book,
                inputs=[book_selector],
                outputs=[manage_message,book_selector,books_output])
    login_button.click(
        fn=login_user,
        inputs=[username_input, password_input],
        outputs=[login_message, books_output, book_selector])
    logout_button.click(
        fn=logout_user,
        inputs=[],
        outputs=[
            login_message,
            books_output,
            book_selector] )
app.launch()