import datetime

from sqlalchemy import Column, ForeignKey, Date, Integer, Float, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=True)
    last_name = Column(String(250), nullable=True)
    email = Column(String(250), nullable=False)
    photo_url = Column(String(750), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        # Returns user data in easily serializeable format
        dict = {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
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
    name = Column(String(250), nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        # Returns genre data in easily serializeable format
        return {
            'id': self.id,
            'name': self.name
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
        'genre_id': self.genre_id
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


engine = create_engine('sqlite:///flask_books.db')
Base.metadata.create_all(engine)

print("Database created!")
