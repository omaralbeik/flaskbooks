from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Genre, Book
from api_errors import APIError

# Connect to the database and create a database session
engine = create_engine('sqlite:///flask_books.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def validateGenre(id):
    if session.query(Genre).filter_by(id=id).all():
        return None
    else:
        return APIError.noGenre

def validateBook(id):
    if session.query(Book).filter_by(id=id).all():
        return None
    else:
        return APIError.noBook


def validateUser(id):
    if session.query(User).filter_by(id=id).all():
        return None
    else:
        return APIError.noUser
