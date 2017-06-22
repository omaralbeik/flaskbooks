from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Genre, Book
from helpers import *

app = Flask(__name__)

# Connect to the database and create a database session
engine = create_engine('sqlite:///bookstore.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


########################################
###          HTML Endpoints          ###
########################################

# show all books
@app.route('/')
@app.route('/books/')
def books():
    return render_books()

# show book info
@app.route('/book/<int:book_id>')
def book(book_id):
    return render_book(book_id)

# show genre
@app.route('/genre/<int:genre_id>/')
def genre(genre_id):
    return render_genre(genre_id)

# show user
@app.route('/user/<int:user_id>/')
def user(user_id):
    return render_user(user_id)

# Add a new book
@app.route('/books/new/', methods=['GET', 'POST'])
def newBook():
    if request.method == 'GET':
        return render_new_book()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        genre_id = request.form['genre_id']
        cover_image_url = request.form['cover_image_url']
        pages_count = request.form['pages_count']
        author_name = request.form['author_name']
        year = request.form['year']
        price = request.form['price']

        if not name:
            flash("Please enter book name")
            return render_new_book()

        if not genre_id:
            flash("Please select a genre")
            return render_new_book()

        book = Book(name=name, genre_id=genre_id, user_id=1)

        book.description = description if description else None
        book.cover_image_url = cover_image_url if cover_image_url else None
        book.pages_count = pages_count if pages_count else None
        book.author_name = author_name if author_name else None
        book.year = year if year else None
        book.price = price if price else None

        session.add(book)
        session.commit()

        return redicrect_books()


# Edit book
@app.route('/book/<int:book_id>/edit/', methods=['GET', 'POST'])
def editBook(book_id):
    if request.method == 'GET':
        return render_edit_book(book_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        genre_id = request.form['genre_id']
        cover_image_url = request.form['cover_image_url']
        pages_count = request.form['pages_count']
        author_name = request.form['author_name']
        year = request.form['year']
        price = request.form['price']

        if not name:
            flash("Please enter book name")
            return render_new_book()

        if not genre_id:
            flash("Please select a genre")
            return render_new_book()

        book = session.query(Book).filter_by(id=book_id).one()

        book.description = description if description else None
        book.cover_image_url = cover_image_url if cover_image_url else None
        book.pages_count = pages_count if pages_count else None
        book.author_name = author_name if author_name else None
        book.year = year if year else None
        book.price = price if price else None

        session.add(book)
        session.commit()

        return redicrect_books()



########################################
###        Render Functions          ###
########################################

def render_books():
    books = session.query(Book).all()
    return render_template('books.html', books=books)

def render_book(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return render_template('book.html', book=book)

def render_new_book():
    genres = session.query(Genre).all()
    return render_template('newbook.html', genres=genres)

def render_edit_book(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    genres = session.query(Genre).all()
    return render_template('editbook.html', book=book, genres=genres)

def render_genre(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    books = session.query(Book).filter_by(genre_id=genre_id)
    return render_template('genre.html', genre=genre, books=books)

def render_user(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    genres = session.query(Genre).filter_by(user_id=user_id).all()
    books = session.query(Book).filter_by(user_id=user_id).all()
    return render_template('user.html', user=user, genres=genres, books=books)


########################################
###       Redicrect Functions        ###
########################################
def redicrect_books():
    return redirect('books')

def redicrect_book(book_id):
        return redirect('book/%s', book_id)

def redicrect_new_book():
    return redicrect('newbook')

def redicrect_edit_book(book_id):
    return redirect('editbook/%s', book_id)

def redicrect_genre(genre_id):
    return redirect('genre/%s', genre_id)

def redicrect_user(user_id):
    return redirect('user/%s', user_id)


########################################
###         JSON Endpoints           ###
########################################

# List all Users
@app.route('/users/JSON')
def usersJSON():
    users = session.query(User).all()
    return jsonify(Users=[u.serialize for u in users])


# List user info
@app.route('/user/<int:user_id>/JSON')
def userJSON(user_id):
    error = validateUser(user_id)
    if error:
        return jsonify(error=error)

    user = session.query(User).filter_by(id=user_id).one()
    genres = session.query(Genre).filter_by(user_id=user_id).all()
    books = session.query(Book).filter_by(user_id=user_id).all()
    return jsonify(user_info=user.serialize,
                   genres=[c.id for c in genres],
                   books=[b.id for b in books])


# List all Genres
@app.route('/genres/JSON')
def genresJSON():
    genres = session.query(Genre).all()
    return jsonify(genres=[c.serialize for c in genres])


# List Genres books
@app.route('/genre/<int:genre_id>/JSON')
def genreBooksJSON(genre_id):
    error = validateGenre(genre_id)
    if error:
        return jsonify(error=error)
    genre = session.query(Genre).filter_by(id=genre_id).one()
    books = session.query(Book).filter_by(genre_id=genre_id).all()
    return jsonify(name=genre.name, books_count=len(books), books=[b.id for b in books])


# List all Books
@app.route('/books/JSON')
def booksJSON():
    books = session.query(Book).all()
    return jsonify(books=[b.serialize for b in books])


# List Book info
@app.route('/book/<int:book_id>/JSON')
def bookJSON(book_id):
    error = validateBook(book_id)
    if error:
        return jsonify(error=error)
    book = session.query(Book).filter_by(id=book_id).one()
    return jsonify(book=book.serialize)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
