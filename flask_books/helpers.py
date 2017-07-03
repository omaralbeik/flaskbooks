from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import render_template, redirect

from model import Base, User, Genre, Book, db_name
from errors import JSONError

# Connect to the database and create a database session
engine = create_engine(db_name)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# TODO fix this after adding auth
temp_user_id = 3



################################################################################
###                            Render Functions                              ###
################################################################################

def render_books(**kwargs):
    books = session.query(Book).all()
    return render_template('books.html',
                           books=books, selected='books', **kwargs)


def render_book(book_id, **kwargs):
    book = session.query(Book).filter_by(id=book_id).one()
    is_liked = temp_user_id in [l.user_id for l in book.likes]
    return render_template('book.html', book=book, selected='books',
                           is_liked=is_liked, **kwargs)


def render_new_book(**kwargs):
    genres = session.query(Genre).all()
    return render_template('newbook.html', genres=genres,
                           selected='books', **kwargs)


def render_edit_book(book_id, **kwargs):
    book = session.query(Book).filter_by(id=book_id).one()
    genres = session.query(Genre).all()
    return render_template('editbook.html', book=book, genres=genres,
                           selected='books', **kwargs)


def render_delete_book(book_id, **kwargs):
    book = session.query(Book).filter_by(id=book_id).one()
    return render_template('deletebook.html', book=book,
                           selected='books', **kwargs)


def render_genres(**kwargs):
    genres = session.query(Genre).all()
    return render_template('genres.html', genres=genres,
                           selected='genres', **kwargs)


def render_genre(genre_id, **kwargs):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    return render_template('genre.html', genre=genre,
                           selected='genres', **kwargs)


def render_new_genre(**kwargs):
    return render_template('newgenre.html', selected='genres', **kwargs)


def render_edit_genre(genre_id, **kwargs):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    return render_template('editgenre.html', genre=genre, **kwargs)


def render_delete_genre(genre_id, **kwargs):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    return render_template('deletegenre.html', genre=genre,
                        selected='genres', **kwargs)


def render_users(**kwargs):
    users = session.query(User).all()
    return render_template('users.html', users=users,
                           selected='users', **kwargs)


def render_user(user_id, **kwargs):
    user = session.query(User).filter_by(id=user_id).one()
    return render_template('user.html', user=user, selected='users', **kwargs)


def render_auth(**kwargs):
    return render_template('auth.html', selected='auth', **kwargs)


################################################################################
###                           Redicrect Functions                            ###
################################################################################

def redicrect_books():
    return redirect('/books/')


def redicrect_book(book_id):
        return redirect('/book/' + str(book_id))


def redicrect_new_book():
    return redicrect('/newbook/')


def redicrect_edit_book(book_id):
    return redirect('/editbook/' + str(book_id))


def redicrect_genres():
    return redirect('/genres/')


def redicrect_genre(genre_id):
    return redirect('/genre/' + str(genre_id))


def redicrect_user(user_id):
    return redirect('/user/' + str(user_id))







def validateGenre(id):
    if session.query(Genre).filter_by(id=id).all():
        return None
    else:
        return JSONError.noGenre

def validateBook(id):
    if session.query(Book).filter_by(id=id).all():
        return None
    else:
        return JSONError.noBook


def validateUser(id):
    if session.query(User).filter_by(id=id).all():
        return None
    else:
        return JSONError.noUser
