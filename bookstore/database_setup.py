from sqlalchemy import Column, ForeignKey, Date, Integer, Float, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    photo_url = Column(String(750), nullable=True)

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


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

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

    @property
    def serialize(self):
        # Returns book data in easily serializeable format
        dict = {
        'id': self.id,
        'name': self.name
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


engine = create_engine('sqlite:///bookstore.db')
Base.metadata.create_all(engine)

print("Database created!")
