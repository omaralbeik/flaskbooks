from flask import Flask, request, flash, jsonify, url_for

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, User, Book, Genre, Like, db_name
from helpers import *
from errors import HTMLError, JSONError

app = Flask(__name__)


# Connect to the database and create a database session
engine = create_engine(db_name)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# TODO fix this after adding auth
temp_user_id = 3



################################################################################
###                              HTML Endpoints                              ###
################################################################################

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
        name = request.form['name'] or None
        description = request.form['description'] or None
        genres_ids = request.form.getlist('genres') or []
        cover_image_url = request.form['cover_image_url'] or None
        page_count = request.form['page_count'] or None
        author_name = request.form['author_name'] or None
        year = request.form['year'] or None

        if not name:
            flash(HTMLError.noBookName, "danger")
            return render_new_book(name=name,
            description=description,
            cover_image_url=cover_image_url,
            page_count=page_count,
            author_name=author_name,
            year=year)

        book = Book(name=name, owner_id=temp_user_id)

        book.description = description
        book.cover_image_url = cover_image_url
        book.page_count = page_count
        book.author_name = author_name
        book.year = year

        genres = []
        for id in genres_ids:
            g = session.query(Genre).filter_by(id=id).one()
            if g:
                genres.append(g)

        book.genres = genres

        session.add(book)
        session.commit()

        return redicrect_books()

# Edit book
@app.route('/book/<int:book_id>/edit/', methods=['GET', 'POST'])
def editBook(book_id):
    if request.method == 'GET':
        return render_edit_book(book_id)

    if request.method == 'POST':
        name = request.form['name'] or None
        description = request.form['description'] or None
        genres_ids = request.form.getlist('genres') or []
        cover_image_url = request.form['cover_image_url'] or None
        page_count = request.form['page_count'] or None
        author_name = request.form['author_name'] or None
        year = request.form['year'] or None

        if not name:
            flash(HTMLError.noBookName, "danger")
            return render_edit_book(book_id=book_id)

        book = session.query(Book).filter_by(id=book_id).one()

        book.name = name
        book.description = description
        book.cover_image_url = cover_image_url
        book.page_count = page_count
        book.author_name = author_name
        book.year = year

        genres = []
        for id in genres_ids:
            g = session.query(Genre).filter_by(id=id).one()
            if g:
                genres.append(g)

        book.genres = []
        book.genres = genres

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

    if validateBook(book_id) or validateUser(temp_user_id):
        return redicrect_book(book_id)

    like = session.query(Like).filter_by(book_id=book_id,
                                         user_id=temp_user_id).all()

    if not like:
        like = Like(book_id=book_id, user_id=temp_user_id)
        session.add(like)
        session.commit()

    return redicrect_book(book_id)

# Dislike a book
@app.route('/book/<int:book_id>/dislike/', methods=['GET', 'POST'])
def dislikeBook(book_id):
    if request.method == 'GET':
        return render_book(book_id)

    if request.method == 'POST':
        if validateBook(book_id) or validateUser(temp_user_id):
            return redicrect_book(book_id)

        like = session.query(Like).filter_by(book_id=book_id,
                                             user_id=temp_user_id).one()

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
    return render_genre(genre_id)

# Show new genre
@app.route('/genres/new/', methods=['GET', 'POST'])
def newGenre():
    if request.method == 'GET':
        return render_new_genre()

    if request.method == 'POST':
        name = request.form['name']

        if not name:
            flash(HTMLError.noGenreName, "danger")
            return render_new_genre()

        if session.query(Genre).filter_by(name=name).one():
            flash(HTMLError.genreExists, "danger")
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
            flash(HTMLError.noBookName, "danger")
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



################################################################################
###                              JSON Endpoints                              ###
################################################################################

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
    return jsonify(book.serialize)


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
    return jsonify(genre.serialize)


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
    return jsonify(user.serialize)




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
