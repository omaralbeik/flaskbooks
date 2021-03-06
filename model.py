import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, Float, String, Text, DateTime
from sqlalchemy.orm import relationship, backref
from flask import url_for, jsonify

db_name = 'sqlite:///flask_books.db'
Base = declarative_base()


genre_book_association_table = Table('genre_book_association', Base.metadata,
    Column('book_id', Integer, ForeignKey('book.id')),
    Column('genre_id', Integer, ForeignKey('genre.id'))
)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    name = Column(String(250), nullable=True)
    bio = Column(String(250), nullable=True)
    picture_url = Column(String(250), nullable=True)
    date_joined = Column(DateTime, default=datetime.datetime.utcnow)

    books = relationship('Book')
    genres = relationship('Genre')
    likes = relationship('Like')

    @property
    def serialize(self):
        # Returns user data in easily serializeable format
        info_dict = {
            'email': self.email,
            'date_joined': self.date_joined
        }
        if self.name:
            info_dict['name'] = self.name
        if self.picture_url:
            info_dict['picture_url'] = self.picture_url
        if self.bio:
            info_dict['bio'] = self.bio

        books_ids = [b.id for b in self.books]
        genres_ids = [g.id for g in self.genres]
        liked_books = [l.book_id for l in self.likes]

        return {
            'id': self.id,
            'user_info': info_dict,
            'books': books_ids,
            'genres': genres_ids,
            'liked_books': liked_books
        }

    @property
    def name_or_email(self):
        return self.name if self.name else self.email

    @property
    def picture_url_or_placeholder(self):
        if self.picture_url:
            return self.picture_url
        else:
            return url_for('static', filename='images/placeholder_user.jpg')



class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(Text, nullable=True)
    cover_image_url = Column(String(750), nullable=True)
    page_count = Column(Integer, nullable=True)
    author_name = Column(String(250), nullable=True)
    year = Column(Integer, nullable=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship(User)

    likes = relationship('Like')
    genres = relationship('Genre',
                          secondary=genre_book_association_table,
                          back_populates='books')


    @property
    def cover_or_placeholder_url(self):
        if self.cover_image_url:
            return self.cover_image_url
        else:
            return url_for('static', filename='images/placeholder_book.jpg')


    @property
    def serialize(self):
        # Returns book data in easily serializeable format

        info_dict = {
            'name': self.name,
            'date_created': self.date_created
        }
        if self.description:
            info_dict['description'] = self.description
        if self.genres:
            info_dict['genres'] = [g.id for g in self.genres]
        if self.cover_image_url:
            info_dict['cover_image_url'] = self.cover_image_url
        if self.page_count:
            info_dict['page_count'] = self.page_count
        if self.author_name:
            info_dict['author_name'] = self.author_name
        if self.year:
            info_dict['year'] = self.year

        social_dict = {
            'likes_count': len(self.likes),
            'owner_id': self.owner_id,
            'date_created': self.date_created
        }

        return {
            'id': self.id, 'book_info': info_dict, 'social': social_dict
        }


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship(User)

    books = relationship('Book',
                          secondary=genre_book_association_table,
                          back_populates='genres')

    @property
    def serialize(self):
        # Returns genre data in easily serializeable format
        info_dict = {
            'name': self.name,
            'book_count': len(self.books)

        }
        books_ids = [b.id for b in self.books]
        return {
            'id': self.id,
            'genre_info': info_dict,
            'books': books_ids
        }


class Like(Base):
    __tablename__ = 'like'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    book_id = Column(Integer, ForeignKey('book.id'))
    book = relationship(Book)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
