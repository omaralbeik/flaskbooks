import random, string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import render_template, redirect, url_for

from model import Base, User, Genre, Book, Like, db_name

import json
from flask import make_response, jsonify

# Connect to the database and create a database session
engine = create_engine(db_name)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(open('client_secrets.json', 'r')
                .read())['web']['client_id']


################################################################################
###                         Database Helper Functions                        ###
################################################################################

###########################  User Helper Functions  ############################
def get_all_users():
    return session.query(User).all()

def get_user_by_id(id):
    try:
        return session.query(User).filter_by(id=id).one()
    except:
        return None


def get_user_by_email(email):
    try:
        return session.query(User).filter_by(email=email).one()
    except:
        return None


def get_user_from_session(login_session):
    email = login_session.get('email')
    if not email:
        return None
    return get_user_by_email(email)


def get_user_id_from_session(login_session):
    user = get_user_from_session(login_session)
    return user.id if user else None


def update_user_info_from_session(login_session):
    name = login_session['name']
    email = login_session['email']
    picture_url = login_session['picture']

    if not email:
        return

    user = get_user_by_email(email)
    if not user:
        return

    user.name = name
    user.picture_url = picture_url
    session.commit()

def create_user(login_session):
    name = login_session['name']
    email = login_session['email']
    picture_url = login_session['picture']

    if get_user_by_email(email):
        return get_user_by_email(email)

    user = User(email=email, name=name, picture_url=picture_url)
    session.add(user)
    session.commit()
    return user


def validate_user(user_id):
    if get_user_by_id(user_id):
        return None
    else:
        return "User doesn't exist"


###########################  Book Helper Functions  ############################
def get_all_books():
    return session.query(Book).all()


def get_book_by_id(id):
    try:
        return session.query(Book).filter_by(id=id).one()
    except:
        return None

def is_book_liked_by_current_user(book_id, login_session):
    user_id = get_user_id_from_session(login_session)
    if not user_id:
        return False
    return True if get_like(book_id, user_id) else False

def validate_book(book_id):
    if get_book_by_id(book_id):
        return None
    else:
        return "Book doesn't exist"


###########################  Genre Helper Functions  ###########################
def get_all_genres():
    return session.query(Genre).all()

def get_genre_by_id(genre_id):
    try:
        return session.query(Genre).filter_by(id=genre_id).one()
    except:
        return None

def get_genre_by_name(name):
    try:
        return session.query(Genre).filter_by(name=name).one()
    except:
        return None

def validate_genre(id):
    if session.query(Genre).filter_by(id=id).all():
        return None
    else:
        return "Genre doesn't exist"


###########################  Like Helper Functions  ############################
def get_like(book_id, user_id):
    return session.query(Like).filter_by(book_id=book_id, user_id=user_id).first()



################################################################################
###                             Auth Functions                               ###
################################################################################

def generate_auth_state():
    choice = string.ascii_uppercase + string.digits
    state = ''.join(random.choice(choice) for x in xrange(32))
    return state

def clear_user_info(login_session):
    login_session.clear()

def save_user_info(login_session, credentials, data):
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = credentials.id_token['sub']
    login_session['provider'] = 'google'
    login_session['name'] = data['name']
    login_session['email'] = data['email']
    login_session['picture'] = data['picture']

    user = get_user_by_email(data['email'])
    if user:
        login_session['user_id'] = user.id
    else:
        create_user_from_session(login_session)

def create_user_from_session(login_session):
    email = login_session.get('email')
    if not email:
        return
    user = User(email=email)
    user.name = login_session.get('name')
    user.picture_url = login_session.get('picture')
    session.add(user)
    session.commit()

def is_user_authenticated(login_session):
    return True if get_user_from_session(login_session) else False

def json_response(error, code):
    response = make_response(json.dumps(error), code)
    response.headers['Content-Type'] = 'application/json'
    return response

def validate_auth(login_session):
    return 'name' in login_session



################################################################################
###                            Render Functions                              ###
################################################################################

def render_books(login_session, **kwargs):
    books = get_all_books()
    current_user = get_user_from_session(login_session)
    return render_template('books.html',
                           books=books,
                           selected='books',
                           current_user=current_user,
                           **kwargs)


def render_book(book_id, login_session, **kwargs):
    book = get_book_by_id(book_id)
    if not book:
        return render_error("Book not found!",
                            login_session,
                            referrer=url_for('books'),
                            button_title="Back to Books")

    current_user = get_user_from_session(login_session)
    is_liked = is_book_liked_by_current_user(book_id, login_session)
    return render_template('book.html',
                           book=book,
                           is_liked=is_liked,
                           current_user=current_user,
                           selected='books', **kwargs)


def render_new_book(login_session, **kwargs):
    if not validate_auth(login_session):
        return render_error("You need to be signed in before adding new books!",
                            login_session,
                            referrer=url_for('auth'),
                            button_title="Login")

    current_user = get_user_from_session(login_session)
    return render_template('newbook.html',
                           genres=get_all_genres(),
                           current_user=current_user,
                           selected='books', **kwargs)


def render_edit_book(book_id, login_session, **kwargs):
    book = get_book_by_id(book_id)
    if not book:
        return render_error("Book not found!",
                            login_session,
                            referrer=url_for('books'),
                            button_title="Back to Books")

    if not validate_auth(login_session):
        return render_error("You need to be signed in before editing books!",
                            login_session,
                            referrer=url_for('auth'),
                            button_title="Login")

    current_user = get_user_from_session(login_session)
    return render_template('editbook.html',
                           book=book,
                           genres=get_all_genres(),
                           current_user=current_user,
                           selected='books',
                           **kwargs)


def render_delete_book(book_id, login_session, **kwargs):
    book = get_book_by_id(book_id)
    if not book:
        return render_error("Book not found!",
                            login_session,
                            referrer=url_for('books'),
                            button_title="Back to Books")

    if not validate_auth(login_session):
        return render_error("You need to be signed in before deleting books!",
                            login_session,
                            referrer=url_for('auth'),
                            button_title="Login")

    current_user_id = get_user_id_from_session(login_session)
    if book.owner_id != current_user_id:
        return render_error("You are not authorized to delete this book.",
                            login_session,
                            referrer=url_for('book', book_id=book_id),
                            button_title="Back to Book's Page")


    current_user = get_user_from_session(login_session)
    return render_template('deletebook.html',
                           book=book,
                           current_user=current_user,
                           selected='books',
                           **kwargs)


def render_genres(login_session, **kwargs):
    current_user = get_user_from_session(login_session)
    return render_template('genres.html',
                           genres=get_all_genres(),
                           current_user=current_user,
                           selected='genres',
                           **kwargs)


def render_genre(genre_id, login_session, **kwargs):
    genre = get_genre_by_id(genre_id)
    current_user = get_user_from_session(login_session)
    if not genre:
        return render_error("Genre not found!",
                            login_session,
                            referrer=url_for('genres'),
                            button_title="Back to Genres")

    return render_template('genre.html',
                           genre=genre,
                           selected='genres',
                           current_user=current_user,
                           **kwargs)


def render_new_genre(login_session, **kwargs):
    if not validate_auth(login_session):
        return render_error("You need to be signed in before adding genres!",
                            login_session,
                            referrer=url_for('auth'),
                            button_title="Login")

    return render_template('newgenre.html',
                           selected='genres',
                           **kwargs)


def render_edit_genre(genre_id, login_session, **kwargs):
    genre = get_genre_by_id(genre_id)
    if not genre:
        return render_error("Genre not found!",
                            login_session,
                            referrer=url_for('genres'),
                            button_title="Back to Genres")

    if not validate_auth(login_session):
        return render_error("You need to be signed in before editing genres!",
                            login_session,
                            referrer=url_for('auth'),
                            button_title="Login")

    return render_template('editgenre.html',
                           genre=genre,
                           **kwargs)


def render_delete_genre(genre_id, login_session, **kwargs):
    genre = get_genre_by_id(genre_id)
    if not genre:
        return render_error("Genre not found!",
                            login_session,
                            referrer=url_for('genres'),
                            button_title="Back to Genres")

    if not validate_auth(login_session):
        return render_error("You need to be signed in before deleting genres!",
                            login_session,
                            referrer=url_for('auth'),
                            button_title="Login")

    current_user_id = get_user_id_from_session(login_session)
    if genre.owner_id != current_user_id:
        return render_error("You are not authorized to delete this genre.",
                            login_session,
                            referrer=url_for('genre', genre_id=genre_id),
                            button_title="Back to Genre's Page")

    return render_template('deletegenre.html',
                           genre=genre,
                           selected='genres',
                           **kwargs)


def render_users(login_session, **kwargs):
    current_user = get_user_from_session(login_session)
    return render_template('users.html',
                           users=get_all_users(),
                           current_user=current_user,
                           selected='users',
                           **kwargs)


def render_user(user_id, login_session, **kwargs):
    user = get_user_by_id(user_id)
    current_user = get_user_from_session(login_session)
    return render_template('user.html',
                           user=user,
                           current_user=current_user,
                           selected='users',
                           **kwargs)


def render_auth(login_session, **kwargs):
    return render_template('auth.html',
                           selected='auth',
                           login_session=login_session,
                           **kwargs)

def render_error(error, login_session, **kwargs):
    current_user = get_user_from_session(login_session)
    return render_template('error.html',
                           error=error,
                           current_user=current_user,
                           **kwargs)


################################################################################
###                           redirect Functions                            ###
################################################################################

def redirect_books():
    return redirect('/books/')


def redirect_book(book_id):
        return redirect('/book/' + str(book_id))


def redirect_new_book():
    return redirect('/newbook/')


def redirect_edit_book(book_id):
    return redirect('/editbook/' + str(book_id))


def redirect_genres():
    return redirect('/genres/')


def redirect_genre(genre_id):
    return redirect('/genre/' + str(genre_id))


def redirect_user(user_id):
    return redirect('/user/' + str(user_id))


def redirect_auth():
    return redirect('/auth/')
