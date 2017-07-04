import httplib2
import requests
import json

from flask import Flask, request, flash, jsonify, url_for
from flask import session as login_session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, User, Book, Genre, Like, db_name
from helpers import *
from errors import HTMLError
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError


app = Flask(__name__)


################################################################################
###                              HTML Endpoints                              ###
################################################################################

# Show all books
@app.route('/')
@app.route('/books/')
def books():
    return render_books(login_session)


# Show book info
@app.route('/book/<int:book_id>')
def book(book_id):
    return render_book(book_id, login_session)


# Add a new book
@app.route('/books/new/', methods=['GET', 'POST'])
def newBook():
    if request.method == 'GET':
        return render_new_book(login_session)

    if request.method == 'POST':

        current_user_id = get_user_id_from_session(login_session)
        if not current_user_id:
            flash(HTMLError.notSignedIn, 'danger')
            return redirect_books(login_session)

        name = request.form['name'] or None
        description = request.form['description'] or None
        genres_ids = request.form.getlist('genres') or []
        cover_image_url = request.form['cover_image_url'] or None
        page_count = request.form['page_count'] or None
        author_name = request.form['author_name'] or None
        year = request.form['year'] or None

        if not name:
            flash(HTMLError.noBookName, 'danger')
            return render_new_book(login_session,
                                   name=name,
                                   description=description,
                                   cover_image_url=cover_image_url,
                                   page_count=page_count,
                                   author_name=author_name,
                                   year=year)

        book = Book(name=name, owner_id=current_user_id)

        book.description = description
        book.cover_image_url = cover_image_url
        book.page_count = page_count
        book.author_name = author_name
        book.year = year

        genres = []
        for id in genres_ids:
            g = get_genre_by_id(id)
            if g:
                genres.append(g)

        book.genres = genres

        session.add(book)
        session.commit()

        return redirect_books()

# Edit book
@app.route('/book/<int:book_id>/edit/', methods=['GET', 'POST'])
def editBook(book_id):
    book = get_book_by_id(book_id)
    current_user_id = get_user_id_from_session(login_session)

    if request.method == 'GET':
        return render_edit_book(book_id, login_session)

    if request.method == 'POST':
        if book.owner_id != current_user_id:
            return redirect_book(book_id, login_session)

        name = request.form['name'] or None
        description = request.form['description'] or None
        genres_ids = request.form.getlist('genres') or []
        cover_image_url = request.form['cover_image_url'] or None
        page_count = request.form['page_count'] or None
        author_name = request.form['author_name'] or None
        year = request.form['year'] or None

        if not name:
            flash(HTMLError.noBookName, 'danger')
            return render_edit_book(book_id, login_session)

        book = get_book_by_id(book_id)

        book.name = name
        book.description = description
        book.cover_image_url = cover_image_url
        book.page_count = page_count
        book.author_name = author_name
        book.year = year

        genres = []
        for id in genres_ids:
            g = get_genre_by_id(id)
            if g:
                genres.append(g)

        book.genres = []
        book.genres = genres

        session.add(book)
        session.commit()

        return redirect_book(book_id)

# Delete book
@app.route('/book/<int:book_id>/delete/', methods=['GET', 'POST'])
def deleteBook(book_id):
    if request.method == 'GET':
        return render_delete_book(book_id, login_session)
    if request.method == 'POST':
        book = get_book_by_id(book_id)
        current_user_id = get_user_id_from_session(login_session)
        if book.owner_id != current_user_id:
            return redirect_book(book_id, login_session)

        session.delete(book)
        session.commit()
        flash("Book deleted!", 'success')
        return redirect_books()


# Like a book
@app.route('/book/<int:book_id>/like/', methods=['GET', 'POST'])
def likeBook(book_id):

    if request.method == 'GET':
        return render_book(book_id, login_session)

    if request.method == 'POST':
        current_user_id = get_user_id_from_session(login_session)
        if not current_user_id:
            return redirect_book(book_id, login_session)

        if validate_book(book_id):
            return redirect_book(book_id, login_session)

        like = get_like(book_id, current_user_id)

        if not like:
            like = Like(book_id=book_id, user_id=current_user_id)
            session.add(like)
            session.commit()

        return redirect_book(book_id)


# Dislike a book
@app.route('/book/<int:book_id>/dislike/', methods=['GET', 'POST'])
def dislikeBook(book_id):
    if request.method == 'GET':
        return render_book(book_id, login_session)

    if request.method == 'POST':
        current_user_id = get_user_id_from_session(login_session)
        if not current_user_id:
            return redirect_book(book_id)

        like = get_like(book_id, current_user_id)
        if like:
            session.delete(like)
            session.commit()

        return redirect_book(book_id)


# Show all genres
@app.route('/genres/')
def genres():
    return render_genres(login_session)

# Show genre
@app.route('/genre/<int:genre_id>/')
def genre(genre_id):
    return render_genre(genre_id, login_session)

# Show new genre
@app.route('/genres/new/', methods=['GET', 'POST'])
def newGenre():
    if request.method == 'GET':
        return render_new_genre(login_session)

    if request.method == 'POST':
        name = request.form['name']

        if not name:
            flash(HTMLError.noGenreName, 'danger')
            return render_new_genre(login_session)

        genre = get_genre_by_name(name)
        if genre:
            flash(HTMLError.genreExists, 'danger')
            return render_new_genre(login_session)

        genre = Genre(name=name, owner_id=get_user_id_from_session(login_session))
        session.add(genre)
        session.commit()
        flash("Genre created!", 'success')
        return redirect_genres()

# Show edit genre
@app.route('/genre/<int:genre_id>/edit/', methods=['GET', 'POST'])
def editGenre(genre_id):

    if request.method == 'GET':
        return render_edit_genre(genre_id, login_session)

    if request.method == 'POST':
        current_user_id = get_user_id_from_session(login_session)
        if book.owner_id != current_user_id:
            return redirect_book(book_id, login_session)

        name = request.form['name']

        if not name:
            flash(HTMLError.noBookName, 'danger')
            return render_new_genre(login_session)

        genre = get_genre_by_id(genre_id)
        genre.name = name
        session.commit()
        flash("Genre updated!", 'success')
        return redirect_genres()


# Delete genre
@app.route('/genre/<int:genre_id>/delete/', methods=['GET', 'POST'])
def deleteGenre(genre_id):
    if request.method == 'GET':
        return render_delete_genre(genre_id, login_session)

    if request.method == 'POST':
        genre = get_genre_by_id(genre_id)
        session.delete(genre)
        session.commit()
        flash("Genre deleted!", 'success')
        return redirect_genres()


# show all users
@app.route('/users/')
def users():
    return render_users(login_session)

# show user
@app.route('/user/<int:user_id>/')
def user(user_id):
    return render_user(user_id, login_session)


# show auth
@app.route('/auth/')
def auth():
    state = generate_auth_state()
    login_session['state'] = state
    return render_auth(login_session, state=state)


################################################################################
###                               Google Auth                                ###
################################################################################

@app.route('/gconnect', methods=['POST'])
def gConnect():

    # Validate state token
    if request.args.get('state') != login_session['state']:
        return json_response('Invalid state parameter.', 401)

    # Obtain authorization code
    code = request.data

    # Upgrade the authorization code into a credentials object
    try:
        oaht_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oaht_flow.redirect_uri = 'postmessage'
        credentials = oaht_flow.step2_exchange(code)

    except FlowExchangeError:
        return json_response('Failed to upgrade the authorization code.', 401)

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           %access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    error = result.get('error')
    if error:
        return json_response(error, 500)

    gplus_id = credentials.id_token['sub']

    # Verify that the access token is used for the intended user.
    if result['user_id'] != gplus_id:
        return json_response("Token's user ID doesn't match given user ID.", 401)

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        return json_response("Token's client ID does not match app's.", 401)


    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        return json_response('Current user is already connected.', 200)

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # Store the access token and user data in the session for later use.
    save_user_info(login_session, credentials, data)
    update_user_info_from_session(login_session)
    return redirect_books()


@app.route('/gdisconnect')
def gDisconnect():
    access_token = login_session.get('access_token')
    if not access_token:
        return json_response('Current user is not connected.', 401)

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' %access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        clear_user_info(login_session)
        login_session.clear()
    	return redirect_books()

    else:
        login_session.clear()
    	return json_response('Failed to revoke token for given user.', 400)



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
    error = validate_book(book_id)
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
    error = validate_genre(genre_id)
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
    error = validate_user(user_id)
    if error:
        return jsonify(error=error)

    user = session.query(User).filter_by(id=user_id).one()
    return jsonify(user.serialize)




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
