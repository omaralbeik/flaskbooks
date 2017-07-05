import httplib2, requests, json

from flask import Flask, request, flash, jsonify, url_for
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

import helpers as h
import dbhelpers as dbh

app = Flask(__name__)

CLIENT_ID = json.load(open('client_secrets.json', 'r'))['web']['client_id']



###############################  HTML Endpoints  ###############################

# Show all books
@app.route('/')
@app.route('/books/')
def books():
    return h.render_books()


# Show book info
@app.route('/book/<int:book_id>')
def book(book_id):
    if not dbh.get_book_by_id(book_id):
        return h.render_book_not_found()
    return h.render_book(book_id)


# Add a new book
@app.route('/books/new/', methods=['GET', 'POST'])
def newBook():
    current_user_id = dbh.get_current_user_id()
    if not current_user_id:
        return h.render_not_authenticated()

    if request.method == 'GET':
        return h.render_new_book()

    if request.method == 'POST':
        name = request.form['name'] or None
        description = request.form['description'] or None
        genres_ids = request.form.getlist('genres') or []
        cover_image_url = request.form['cover_image_url'] or None
        page_count = request.form['page_count'] or None
        author_name = request.form['author_name'] or None
        year = request.form['year'] or None

        if not name:
            flash('Please enter book name and try again.', 'danger')
            return h.render_new_book(name=name,
                                     description=description,
                                     cover_image_url=cover_image_url,
                                     page_count=page_count,
                                     author_name=author_name,
                                     year=year)

        book = dbh.create_book(name=name,
                               description=description,
                               genres_ids=genres_ids,
                               cover_image_url=cover_image_url,
                               page_count=page_count,
                               author_name=author_name,
                               year=year)

        if book:
            flash('Book Added!', 'success')
            return h.redirect_books()


# Edit book
@app.route('/book/<int:book_id>/edit/', methods=['GET', 'POST'])
def editBook(book_id):
    if not dbh.get_book_by_id(book_id):
        return h.render_book_not_found()
    current_user_id = dbh.get_current_user_id()
    if not current_user_id:
        return h.render_not_authenticated()
    if dbh.get_book_by_id(book_id).owner_id != current_user_id:
        return h.render_not_authorized()

    if request.method == 'GET':
        return h.render_edit_book(book_id)

    if request.method == 'POST':
        name = request.form['name'] or None
        description = request.form['description'] or None
        genres_ids = request.form.getlist('genres') or []
        cover_image_url = request.form['cover_image_url'] or None
        page_count = request.form['page_count'] or None
        author_name = request.form['author_name'] or None
        year = request.form['year'] or None

        if not name:
            flash('Please enter book name and try again.', 'danger')
            return h.render_edit_book(book_id)

        book = dbh.update_book(book_id,
                               name=name,
                               description=description,
                               genres_ids=genres_ids,
                               cover_image_url=cover_image_url,
                               page_count=page_count,
                               author_name=author_name,
                               year=year)

        if book:
            flash('Book Updated!', 'success')
            return h.redirect_book(book_id)


# Delete book
@app.route('/book/<int:book_id>/delete/', methods=['GET', 'POST'])
def deleteBook(book_id):
    if not dbh.get_book_by_id(book_id):
        return h.render_book_not_found()
    current_user_id = dbh.get_current_user_id()
    if not current_user_id:
        return h.render_not_authenticated()
    if dbh.get_book_by_id(book_id).owner_id != current_user_id:
        return h.render_not_authorized()

    if request.method == 'GET':
        return h.render_delete_book(book_id)

    if request.method == 'POST':
        dbh.delete_book(book_id)
        flash('Book Deleted!', 'success')
        return h.redirect_books()



# Like a book
@app.route('/book/<int:book_id>/like/', methods=['GET', 'POST'])
def likeBook(book_id):
    current_user_id = dbh.get_current_user_id()
    if not current_user_id:
        return h.render_not_authenticated()

    if request.method == 'GET':
        return h.render_book(book_id)

    if request.method == 'POST':
        like = dbh.like_book(book_id)
        if like:
            return h.redirect_book(book_id)


# Dislike a book
@app.route('/book/<int:book_id>/dislike/', methods=['GET', 'POST'])
def dislikeBook(book_id):
    current_user_id = dbh.get_current_user_id()
    if not current_user_id:
        return h.render_not_authenticated()

    if request.method == 'GET':
        return h.render_book(book_id)

    if request.method == 'POST':
        like = dbh.dislike_book(book_id)
        return h.redirect_book(book_id)


# Show all genres
@app.route('/genres/')
def genres():
    return h.render_genres()


# Show genre
@app.route('/genre/<int:genre_id>/')
def genre(genre_id):
    if not dbh.get_genre_by_id(genre_id):
        return h.render_genre_not_found()
    return h.render_genre(genre_id)


# Show new genre
@app.route('/genres/new/', methods=['GET', 'POST'])
def newGenre():
    current_user_id = dbh.get_current_user_id()
    if not current_user_id:
        return h.render_not_authenticated()

    if request.method == 'GET':
        return h.render_new_genre()

    if request.method == 'POST':
        name = request.form['name']

        if not name:
            flash('Please enter genre name and try again.', 'danger')
            return h.render_new_genre()

        if dbh.get_genre_by_name(name):
            flash("Genre exist, try another name!", 'danger')
            return h.render_new_genre()

        genre = dbh.create_genre(name)
        if genre:
            flash("Genre created!", 'success')
            return h.redirect_genres()


# Show edit genre
@app.route('/genre/<int:genre_id>/edit/', methods=['GET', 'POST'])
def editGenre(genre_id):
    if not dbh.get_genre_by_id(genre_id):
        return h.render_genre_not_found()
    current_user_id = dbh.get_current_user_id()
    if not current_user_id:
        return h.render_not_authenticated()
    if dbh.get_genre_by_id(genre_id).owner_id != current_user_id:
        return h.render_not_authorized()

    if request.method == 'GET':
        return h.render_edit_genre(genre_id)

    if request.method == 'POST':
        name = request.form['name']
        if not name:
            flash('Please enter genre name and try again.', 'danger')
            return h.render_new_genre()

        if dbh.get_genre_by_name(name):
            flash("Genre exist, try another name!", 'danger')
            return h.render_new_genre()

        genre = dbh.create_genre(name)
        if genre:
            flash("Genre updated!", 'success')
            return h.redirect_genre(genre_id)


# Delete genre
@app.route('/genre/<int:genre_id>/delete/', methods=['GET', 'POST'])
def deleteGenre(genre_id):
    if not dbh.get_genre_by_id(genre_id):
        return h.render_genre_not_found()
    current_user_id = dbh.get_current_user_id()
    if not current_user_id:
        return h.render_not_authenticated()
    if dbh.get_genre_by_id(genre_id).owner_id != current_user_id:
        return h.render_not_authorized()

    if request.method == 'GET':
        return h.render_delete_genre(genre_id)

    if request.method == 'POST':
        dbh.delete_genre(genre_id)
        flash("Genre deleted!", 'success')


# show all users
@app.route('/users/')
def users():
    return h.render_users()

# show user
@app.route('/user/<int:user_id>/')
def user(user_id):
    if not dbh.get_user_by_id(user_id):
        return h.render_user_not_found()
    return h.render_user(user_id)


# show auth
@app.route('/auth/')
def auth():
    state = h.generate_auth_state()
    login_session['state'] = state
    return h.render_auth(state=state, CLIENT_ID=CLIENT_ID)


@app.errorhandler(404)
def showError(e):
  return h.render_not_found(), 404



################################  Google Auth  #################################

@app.route('/gconnect', methods=['POST'])
def gConnect():

    # Validate state token
    if request.args.get('state') != login_session['state']:
        return h.json_response('Invalid state parameter.', 401)

    # Obtain authorization code
    code = request.data

    # Upgrade the authorization code into a credentials object
    try:
        oaht_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oaht_flow.redirect_uri = 'postmessage'
        credentials = oaht_flow.step2_exchange(code)

    except FlowExchangeError:
        return h.json_response('Failed to upgrade the authorization code.', 401)

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           %access_token)
    http = httplib2.Http()
    result = json.loads(http.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    error = result.get('error')
    if error:
        return h.json_response(error, 500)

    gplus_id = credentials.id_token['sub']

    # Verify that the access token is used for the intended user.
    if result['user_id'] != gplus_id:
        return h.json_response("Token's user ID doesn't match given user ID.", 401)

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        return h.json_response("Token's client ID does not match app's.", 401)

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        return h.json_response('Current user is already connected.', 200)

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # Store the access token and user data in the session for later use.
    h.save_current_user_info(credentials, data)

    user = dbh.create_or_update_current_user_from_login_session()
    if user:
        return h.redirect_books()


@app.route('/gdisconnect')
def gDisconnect():
    access_token = login_session.get('access_token')
    if not access_token:
        return h.json_response('Current user is not connected.', 401)

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' %access_token
    http = httplib2.Http()
    result = http.request(url, 'GET')[0]

    if result['status'] == '200':
        h.clear_login_session()
    	return h.redirect_books()

    else:
        h.clear_login_session()
    	return h.json_response('Failed to revoke token for given user.', 400)



################################################################################
###                              JSON Endpoints                              ###
################################################################################

# List all Books
@app.route('/books/JSON')
def booksJSON():
    return jsonify(books=[b.serialize for b in dbh.get_all_books()])


# List Book info
@app.route('/book/<int:book_id>/JSON')
def bookJSON(book_id):
    book = dbh.get_book_by_id(book_id)
    if not book:
        return h.json_response("Book doesn't exist", 404)
    return jsonify(dbh.get_book_by_id(book_id).serialize)


# List all Genres
@app.route('/genres/JSON')
def genresJSON():
    return jsonify(genres=[g.serialize for g in dbh.get_all_genres()])


# List Genres books
@app.route('/genre/<int:genre_id>/JSON')
def genreJSON(genre_id):
    genre = dbh.get_genre_by_id(genre_id)
    if not genre:
        return h.json_response("Genre doesn't exist", 404)
    return jsonify(genre.serialize)


# List all Users
@app.route('/users/JSON')
def usersJSON():
    return jsonify(Users=[u.serialize for u in dbh.get_all_users()])


# List user info
@app.route('/user/<int:user_id>/JSON')
def userJSON(user_id):
    user = dbh.get_user_by_id(user_id)
    if not user:
        return h.json_response("User doesn't exist", 404)
    return jsonify(user.serialize)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.register_error_handler(404, showError)
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
