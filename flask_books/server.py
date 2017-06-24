from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Genre, Book, Like
from helpers import *

app = Flask(__name__)

# Connect to the database and create a database session
engine = create_engine('sqlite:///flask_books.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


########################################
###          HTML Endpoints          ###
########################################

# Show all books
@app.route('/')
@app.route('/books/')
def books():
    return render_books()

# Show book info
@app.route('/book/<int:book_id>')
def book(book_id):
    return render_book(book_id)

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
            flash("Please enter book name", "danger")
            return render_new_book(name=name,
            description=description,
            genre_id=genre_id,
            cover_image_url=cover_image_url,
            pages_count=pages_count,
            author_name=author_name,
            year=year,
            price=price)

        if not genre_id:
            flash("Please select a genre", "danger")
            return render_new_book(name=name,
            description=description,
            genre_id=genre_id,
            cover_image_url=cover_image_url,
            pages_count=pages_count,
            author_name=author_name,
            year=year,
            price=price)

        book = Book(name=name, genre_id=genre_id, user_id=2)

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
            flash("Please enter book name", "danger")
            return render_edit_book(book_id=book_id)

        if not genre_id:
            flash("Please select a genre", "danger")
            return render_edit_book(book_id=book_id)

        book = session.query(Book).filter_by(id=book_id).one()

        book.genre_id = genre_id
        book.description = description if description else None
        book.cover_image_url = cover_image_url if cover_image_url else None
        book.pages_count = pages_count if pages_count else None
        book.author_name = author_name if author_name else None
        book.year = year if year else None
        book.price = price if price else None

        session.add(book)
        session.commit()

        return redicrect_books()

# Delete book
@app.route('/book/<int:book_id>/delete/', methods=['GET', 'POST'])
def deleteBook(book_id):
    if request.method == 'GET':
        return render_delete_book(book_id)

    if request.method == 'POST':
        book = session.query(Book).filter_by(id=book_id).one()
        session.delete(book)
        session.commit()
        flash("Book deleted!", "success")
        return redicrect_books()


# Like a book
@app.route('/book/<int:book_id>/like/', methods=['GET', 'POST'])
def likeBook(book_id):
    if request.method == 'GET':
        return render_book(book_id)

    if validateBook(book_id) or validateUser(2):
        return redicrect_book(book_id)

    like = session.query(Like).filter_by(book_id=book_id, user_id=2).all()

    if not like:
        like = Like(book_id=book_id, user_id=2)
        session.add(like)
        session.commit()

    return redicrect_book(book_id)

# Dislike a book
@app.route('/book/<int:book_id>/dislike/', methods=['GET', 'POST'])
def dislikeBook(book_id):
    if request.method == 'GET':
        return render_book(book_id)

    if request.method == 'POST':
        if validateBook(book_id) or validateUser(2):
            return redicrect_book(book_id)

        like = session.query(Like).filter_by(book_id=book_id, user_id=2).one()

        if like:
            session.delete(like)
            session.commit()

        return redicrect_book(book_id)


# Show all genres
@app.route('/genres/')
def genres():
    return render_genres()

# Show genre
@app.route('/genre/<int:genre_id>/')
def genre(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    return render_genre(genre_id, books=genre.books)

# Show new genre
@app.route('/genres/new/', methods=['GET', 'POST'])
def newGenre():
    if request.method == 'GET':
        return render_new_genre()

    if request.method == 'POST':
        name = request.form['name']

        if not name:
            flash("Please enter genre name", "danger")
            return render_new_genre()

        if session.query(Genre).filter_by(name=name).one():
            flash("Genre already exist!", "danger")
            return render_new_genre()

        genre = Genre(name=name, user_id=1)
        session.add(genre)
        session.commit()
        flash("Genre created!", "success")
        return redicrect_genres()

# Show edit genre
@app.route('/genre/<int:genre_id>/edit/', methods=['GET', 'POST'])
def editGenre(genre_id):
    if request.method == 'GET':
        return render_edit_genre(genre_id)

    if request.method == 'POST':
        name = request.form['name']

        if not name:
            flash("Please enter book name", "danger")
            return render_new_genre()

        genre = session.query(Genre).filter_by(id=genre_id).one()
        genre.name = name
        session.commit()
        flash("Genre updated!", "success")
        return redicrect_genres()

# Delete genre
@app.route('/genre/<int:genre_id>/delete/', methods=['GET', 'POST'])
def deleteGenre(genre_id):
    if request.method == 'GET':
        return render_delete_genre(genre_id)

    if request.method == 'POST':
        genre = session.query(Genre).filter_by(id=genre_id).one()
        session.delete(genre)
        session.commit()
        flash("Genre deleted!", "success")
        return redicrect_genres()



# show all users
@app.route('/users/')
def users():
    return render_users()

# show user
@app.route('/user/<int:user_id>/')
def user(user_id):
    return render_user(user_id)


# show auth
@app.route('/auth/')
def auth():
    return render_auth()


@app.route('/auth/signin', methods=['POST'])
def signIn():
    email = request.form['email']
    password = request.form['password']

    if not email:
        flash("Please enter your email!", "danger")
        return render_auth()

    if not password:
        flash("Please enter your password!", "danger")
        return render_auth()

    flash("Signed In!", "success")
    return redicrect_books()

@app.route('/auth/signup', methods=['POST'])
def signUp():

    firstName = request.form['first_name']
    lastName = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['password2']

    if not email:
        flash("Please enter your email!", "danger")
        return render_auth()

    if not password:
        flash("Please enter your password!", "danger")
        return render_auth()

    if not password2:
        flash("Passwords don't match", "danger")
        return render_auth()

    if password != password2:
        flash("Passwords don't match", "danger")
        return render_auth()

    flash("Signed Up!", "success")
    return redicrect_books()


########################################
###        Render Functions          ###
########################################

def render_books():
    books = session.query(Book).all()
    return render_template('books.html', books=books, selected='books')

def render_book(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    likes = session.query(Like).filter_by(book_id=book_id).all()
    user = session.query(User).filter_by(id=2).one()
    liked_ids = [l.book_id for l in user.likes]
    is_liked = book_id in liked_ids
    return render_template('book.html', book=book, selected='books', likes_count=len(likes), is_liked=is_liked)

def render_new_book(**kwargs):
    genres = session.query(Genre).all()
    return render_template('newbook.html', genres=genres, selected='books', **kwargs)

def render_edit_book(book_id, **kwargs):
    book = session.query(Book).filter_by(id=book_id).one()
    genres = session.query(Genre).all()
    return render_template('editbook.html', book=book, genres=genres, selected='books', **kwargs)

def render_delete_book(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return render_template('deletebook.html', book=book, selected='books')



def render_genres():
    genres = session.query(Genre).all()
    books = session.query(Book).all()
    counts = dict()
    for b in books:
        counts[b.genre_id] = counts.get(b.genre_id, 0) + 1
    return render_template('genres.html', genres=genres, books_count=counts, selected='genres')

def render_genre(genre_id, **kwargs):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    books = session.query(Book).filter_by(genre_id=genre_id)
    return render_template('genre.html', genre=genre, selected='genres', **kwargs)

def render_new_genre(**kwargs):
    return render_template('newgenre.html', selected='genres', **kwargs)

def render_edit_genre(genre_id, **kwargs):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    return render_template('editgenre.html', genre=genre, **kwargs)

def render_delete_genre(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    return render_template('deletegenre.html', genre=genre, selected='genres')



def render_users():
    users = session.query(User).all()
    return render_template('users.html', users=users, selected='users')

def render_user(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return render_template('user.html', user=user,
                                        books=user.books,
                                        genres=user.genres,
                                        liked_books=[l.book for l in user.likes],
                                        selected='users')

def render_auth():
    return render_template('auth.html', selected='auth')

########################################
###       Redicrect Functions        ###
########################################
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


########################################
###         JSON Endpoints           ###
########################################

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
    likes = session.query(Like).filter_by(book_id=book_id).all()
    social = {
    'likes_count': len(likes),
    'owner_id': book.user_id,
    'created_at': book.created_at
    }
    return jsonify(book_info=book.serialize, social=social)


# List all Genres
@app.route('/genres/JSON')
def genresJSON():
    genres = session.query(Genre).all()
    return jsonify(genres=[c.serialize for c in genres])


# List Genres books
@app.route('/genre/<int:genre_id>/JSON')
def genreJSON(genre_id):
    error = validateGenre(genre_id)
    if error:
        return jsonify(error=error)
    genre = session.query(Genre).filter_by(id=genre_id).one()
    return jsonify(name=genre.name, books_count=len(genre.books), books=[b.id for b in genre.books])


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
    return jsonify(user_info=user.serialize,
                   genres=[g.id for g in user.genres],
                   books=[b.id for b in user.books],
                   liked_books=[l.book_id for l in user.likes])



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
