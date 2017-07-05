import random, string, json

from flask import render_template, redirect, make_response, url_for

from application import login_session
import dbhelpers as dbh


################################ Auth Functions ################################

def generate_auth_state():
    choice = string.ascii_uppercase + string.digits
    state = ''.join(random.choice(choice) for x in xrange(32))
    return state


def clear_login_session():
    login_session.clear()


def save_current_user_info(credentials, data):
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = credentials.id_token['sub']
    login_session['provider'] = 'google'
    login_session['name'] = data['name']
    login_session['email'] = data['email']
    login_session['picture'] = data['picture']



##############################  Render Functions  ##############################

def render_books(**kwargs):
    return render_template('books.html',
                           books=dbh.get_all_books(),
                           current_user= dbh.get_current_user(),
                           selected='books',
                           **kwargs)


def render_book(book_id, **kwargs):
    return render_template('book.html',
                           book=dbh.get_book_by_id(book_id),
                           current_user = dbh.get_current_user(),
                           is_liked = dbh.is_book_liked_by_current_user(book_id),
                           selected='books',
                           **kwargs)


def render_new_book(**kwargs):
    return render_template('newbook.html',
                           genres=dbh.get_all_genres(),
                           current_user=dbh.get_current_user(),
                           selected='books',
                           **kwargs)


def render_edit_book(book_id, **kwargs):
    return render_template('editbook.html',
                           book=dbh.get_book_by_id(book_id),
                           genres=dbh.get_all_genres(),
                           current_user=dbh.get_current_user(),
                           selected='books',
                           **kwargs)


def render_delete_book(book_id, **kwargs):
    return render_template('deletebook.html',
                           book=dbh.get_book_by_id(book_id),
                           current_user=dbh.get_current_user(),
                           selected='books',
                           **kwargs)


def render_genres(**kwargs):
    return render_template('genres.html',
                           genres=dbh.get_all_genres(),
                           current_user=dbh.get_current_user(),
                           selected='genres',
                           **kwargs)


def render_genre(genre_id, **kwargs):
    return render_template('genre.html',
                           genre=dbh.get_genre_by_id(genre_id),
                           current_user=dbh.get_current_user(),
                           selected='genres',
                           **kwargs)


def render_new_genre(**kwargs):
    return render_template('newgenre.html',
                           current_user=dbh.get_current_user(),
                           selected='genres',
                           **kwargs)


def render_edit_genre(genre_id, **kwargs):
    return render_template('editgenre.html',
                           genre=dbh.get_genre_by_id(genre_id),
                           current_user=dbh.get_current_user(),
                           selected='genres',
                           **kwargs)


def render_delete_genre(genre_id, **kwargs):
    return render_template('deletegenre.html',
                           genre=dbh.get_genre_by_id(genre_id),
                           current_user=dbh.get_current_user(),
                           selected='genres',
                           **kwargs)


def render_users(**kwargs):
    return render_template('users.html',
                           users=dbh.get_all_users(),
                           current_user=dbh.get_current_user(),
                           selected='users',
                           **kwargs)


def render_user(user_id, **kwargs):
    return render_template('user.html',
                           user=dbh.get_user_by_id(user_id),
                           current_user=dbh.get_current_user(),
                           selected='users',
                           **kwargs)

def render_edit_user(user_id, **kwargs):
    return render_template('edituser.html',
                           user=dbh.get_user_by_id(user_id),
                           current_user=dbh.get_current_user(),
                           **kwargs)

def render_auth(**kwargs):
    return render_template('auth.html',
                           login_session=login_session,
                           current_user=dbh.get_current_user(),
                           selected='auth',
                           **kwargs)


def render_error(error, **kwargs):
    return render_template('error.html',
                           error=error,
                           current_user=dbh.get_current_user(),
                           **kwargs)

def render_not_found(**kwargs):
    return render_error(error='Page not found, aka 404',
                        referrer='/',
                        button_title="Return to Home",
                        **kwargs)


def render_not_authenticated(**kwargs):
    return render_error("You need to sign in before accessing this page",
                        referrer=url_for('auth'),
                        button_title="Login",
                        **kwargs)


def render_not_authorized(**kwargs):
    return render_error("You are not authorized to access this page",
                        referrer='/',
                        button_title="Return to Home",
                        **kwargs)


def render_book_not_found(**kwargs):
    return render_error("Book doesn't exist",
                        referrer=url_for('books'),
                        button_title="Return to Books",
                        **kwargs)


def render_genre_not_found(**kwargs):
    return render_error("Genre doesn't exist",
                        referrer=url_for('genres'),
                        button_title="Return to Genres",
                        **kwargs)


def render_user_not_found(**kwargs):
    return render_error("User doesn't exist",
                        referrer=url_for('users'),
                        button_title="Return to Users",
                        **kwargs)



############################## redirect Functions ##############################

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



###############################  Misc Functions  ###############################

def json_response(error, code):
    response = make_response(json.dumps(error), code)
    response.headers['Content-Type'] = 'application/json'
    return response
