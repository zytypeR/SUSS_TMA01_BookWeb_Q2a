# app.py

from flask import Flask, render_template, redirect, url_for, Blueprint, request
# Assuming flask_login, current_user, etc. are imported if you're using a full app context
from flask_login import current_user, LoginManager
from models.books import Book # Import the model we just created

# --- 1. SETUP (Adapted from __init__.py) ---

def create_app():
    app = Flask(__name__)
    # Dummy config for secret key and static folder (based on your original setup)
    app.config['SECRET_KEY'] = 'your_strong_secret_key' 
    app.static_folder = 'assets' 
    
    # Placeholder for LoginManager setup (if needed later)
    # login_manager = LoginManager()
    # login_manager.init_app(app)
    
    # Create a dummy current_user for template rendering without full login setup
    # If the app runs without a logged-in user, current_user.is_authenticated will be False
    class DummyUser:
        is_authenticated = False
    
    app.jinja_env.globals['current_user'] = DummyUser()
    
    return app

app = create_app()

# --- 2. BLUEPRINT (CONTROLLER) ---

# Define the Blueprint for book-related routes
book = Blueprint('book', __name__, template_folder='templates')

# Route for the main Book Titles page
@book.route('/booktitles', methods=['GET'])
def book_titles():
    # 1. Get the category filter value from the URL query string
    #    Default to 'All' if the filter is not present
    selected_category = request.args.get('category', 'All') 
    
    # 2. Fetch data, passing the selected category to the model
    # 🚨 CRITICAL CHANGE 3: Pass the filter to the model method
    all_books = Book.getAllBooks(category_filter=selected_category)
    
    # 3. Render the template
    # 🚨 CRITICAL CHANGE 4: Pass the selected category back to the template
    return render_template ('book_titles.html',
                        all_books=all_books,
                        selected_category=selected_category,
                        panel="BOOK TITLES")

# Route for the Book Details page
@book.route('/viewBookDetail/<title>')
def view_book_detail(title):
    # 1. Retrieve the specific book data using the title from the URL
    book_details = Book.getBookByTitle(title)

    # 2. Handle case where book is not found
    if book_details is None:
        # Redirect to the main list or show a 404 error
        return redirect(url_for('book.book_titles'))

    # 3. Render the new template
    return render_template('book_details.html',
                           book=book_details,
                           panel="BOOK DETAILS")

# --- 3. REGISTER BLUEPRINT AND ROOT ROUTE ---

app.register_blueprint(book)

# Set the application to open on the Book Titles page (Requirement 3)
@app.route('/')
def home():
    # Redirects the root URL to the book titles page URL (book.book_titles)
    return redirect(url_for('book.book_titles'))


if __name__ == '__main__':
    print("Running SG Library...")
    # NOTE: Ensure your folder structure is correct: 
    # book_web_app.py, models/books.py, templates/book_titles.html, assets/css/custom.css
    app.run(debug=True)