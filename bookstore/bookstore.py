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
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
