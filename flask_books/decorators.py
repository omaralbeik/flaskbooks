from functools import wraps

import helpers as h
import dbhelpers as dbh

def require_authentication(func):
    @wraps(func)
    def wrapper():
        current_user_id = dbh.get_current_user_id()
        if not current_user_id:
            return h.render_not_authenticated()
        else:
            return func()
    return wrapper

def if_authorized_for_book(book_id):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            book = dbh.get_book_by_id(kwargs['book_id'])
            user_id = dbh.get_current_user_id()
            if book.owner_id != user_id:
                return h.render_not_authorized()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def if_authorized_for_genre(genre_id):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            genre = dbh.get_genre_by_id(kwargs['genre_id'])
            user_id = dbh.get_current_user_id()
            if genre.owner_id != user_id:
                return h.render_not_authorized()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def if_authorized_for_user(user_id):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = dbh.get_user_by_id(kwargs['user_id'])
            user_id = dbh.get_current_user_id()
            if user.id != user_id:
                return h.render_not_authorized()
            return func(*args, **kwargs)
        return wrapper
    return decorator


def if_book_available(book_id):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            book = dbh.get_book_by_id(kwargs['book_id'])
            if not book:
                return h.render_book_not_found()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def if_genre_available(genre_id):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            book = dbh.get_genre_by_id(kwargs['genre_id'])
            if not book:
                return h.render_genre_not_found()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def if_user_available(user_id):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            book = dbh.get_user_by_id(kwargs['user_id'])
            if not book:
                return h.render_user_not_found()
            return func(*args, **kwargs)
        return wrapper
    return decorator
