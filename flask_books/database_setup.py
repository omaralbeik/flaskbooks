import datetime

from sqlalchemy import Column, ForeignKey, Date, Integer, Float, String, Text, DateTime, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    first_name = Column(String(250), nullable=True)
    last_name = Column(String(250), nullable=True)
    photo_url = Column(String(750), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    books = relationship('Book', backref='owner', lazy=True)
    genres = relationship('Genre', backref='owner', lazy=True)

    likes = relationship('Like', backref='owner', lazy=True)

    @property
    def serialize(self):
        # Returns user data in easily serializeable format
        dict = {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at
        }
        if self.first_name:
            dict["first_name"] = self.first_name
        if self.last_name:
            dict["last_name"] = self.last_name
        if self.photo_url:
            dict["photo_url"] = self.photo_url
        return dict

    def name(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        else:
            return self.email

class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        # Returns genre data in easily serializeable format
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at
        }


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(Text, nullable=True)
    cover_image_url = Column(String(750), nullable=True)
    pages_count = Column(Integer, nullable=True)
    author_name = Column(String(250), nullable=True)
    year = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)

    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship(Genre)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        # Returns book data in easily serializeable format
        dict = {
        'id': self.id,
        'name': self.name,
        'genre_id': self.genre_id,
        }
        if self.description:
            dict['description'] = self.description
        if self.cover_image_url:
            dict['cover_image_url'] = self.cover_image_url
        if self.pages_count:
            dict['pages_count'] = self.pages_count
        if self.author_name:
            dict['author_name'] = self.author_name
        if self.year:
            dict['year'] = self.year
        if self.price:
            dict['price'] = self.price
        return dict

class Like(Base):
    __tablename__ = 'like'

    id = Column(Integer, primary_key=True)

    book_id = Column(Integer, ForeignKey('book.id'))
    book = relationship(Book)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)


engine = create_engine('sqlite:///flask_books.db')
Base.metadata.create_all(engine)

print("Database created!")
