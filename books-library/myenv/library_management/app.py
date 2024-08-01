from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

inventory = []
borrowed_books = {}

borrowed_path = 'data/borrowed_books.json'
inventory_path = 'data/library_inventory.json'

# Create the file if it doesn't exist
if not os.path.isfile(inventory_path):
    with open(inventory_path, 'w') as f:
        json.dump(inventory, f)

if not os.path.isfile(borrowed_books_path):
    with open(borrowed_books_path, 'w') as f:
        json.dump(borrowed_books, f)

with open(inventory_path, 'r') as f:
    inventory_path = json.load(f)

with open(borrowed_books_path, 'r') as f:
    borrowed_books = json.load(f)

# Step 2: Define the Functions
def add_book(title, author):
    book = {"title": title, "author": author}
    inventory.append(book)
    save_data()

def remove_book(title):
    global inventory
    inventory = [book for book in inventory if book["title"] != title]
    save_data()

def search_book(title):
    for book in inventory:
        if book["title"].lower() == title.lower():
            return book
    return None

def borrow_book(title, borrower):
    for book in inventory:
        if book["title"].lower() == title.lower():
            borrowed_books[title] = borrower
            inventory.remove(book)
            save_data()
            return True
    return False

def return_book(title):
    if title in borrowed_books:
        borrower = borrowed_books.pop(title)
        add_book(title, "Unknown")
        save_data()
        return True
    return False

def save_data():
    print(inventory_path)
    with open('/app/data/borrowed_books.json', 'w') as f:
        json.dump(inventory, f)
    with open(borrowed_books_path, 'w') as f:
        json.dump(borrowed_books, f)
@app.route('/')
def index():
    return render_template('index.html', library_inventory=inventory)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        add_book(title, author)
        #flash('Book added successfully!')
        flash('This should appear')
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        title = request.form['title']
        remove_book(title)
        flash('Book removed successfully!')
        return redirect(url_for('index'))
    return render_template('remove_book.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        title = request.form['title']
        book = search_book(title)
        if book:
            flash(f'Found book: "{book["title"]}" by {book["author"]}')
        else:
            flash('Book not found.')
        return redirect(url_for('index'))
    return render_template('search_book.html')

@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    if request.method == 'POST':
        title = request.form['title']
        borrower = request.form['borrower']
        if borrow_book(title, borrower):
            flash('Book borrowed successfully!')
        else:
            flash('Book not available.')
        return redirect(url_for('index'))
    return render_template('borrow_book.html')

@app.route('/return', methods=['GET', 'POST'])
def return_book_route():
    """
    """
    if request.method == 'POST':
        title = request.form['title']
        if return_book(title):
            flash('Book returned successfully!')
        else:
            flash('Book was not borrowed.')
        return redirect(url_for('index'))
    return render_template('return_book.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
