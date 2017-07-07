from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, User, Genre, Book, Like, db_name


from application import login_session

# Connect to the database and create a database session
engine = create_engine(db_name)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



###########################  User Helper Functions  ############################

def create_user(email, name, picture_url, bio):
    if get_user_by_email(email):
        return False
    user = User(email=email, name=name, picture_url=picture_url, bio=bio)
    session.add(user)
    session.commit()
    return user


def create_user_from_login_session():
    name = login_session['name']
    email = login_session['email']
    picture_url = login_session['picture']
    if not email:
        return False
    user = get_user_by_email(email)
    if user:
        return user
    user = create_user(email, name, picture_url, bio=None)
    return user


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


def get_current_user():
    email = login_session.get('email')
    return get_user_by_email(email) if email else None


def get_current_user_id():
    user = get_current_user()
    return user.id if user else None


def update_current_user_info(**kwargs):
    user = get_current_user()
    if not user:
        return False
    name = kwargs.get('name')
    bio = kwargs.get('bio')
    picture_url = kwargs.get('picture_url')
    if name:
        user.name = name
    if bio:
        user.bio = bio
    if picture_url:
        user.picture_url = picture_url
    session.add(user)
    session.commit()
    return user


def update_current_user_info_from_login_session():
    name = login_session['name']
    email = login_session['email']
    picture_url = login_session['picture']
    if not email:
        return False
    user = get_user_by_email(email)
    if not user:
        return False
    user.name = name
    user.picture_url = picture_url
    session.add(user)
    session.commit()
    return user

def create_or_update_current_user_from_login_session():
    email = login_session['email']
    user = get_user_by_email(email)
    if user:
        update_current_user_info_from_login_session()
        return user
    else:
        return create_user_from_login_session()


def delete_current_user():
    user = get_current_user()
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True



###########################  Book Helper Functions  ############################

def create_book(name, **kwargs):
    owner_id = get_current_user_id()
    if not owner_id:
        return False
    description = kwargs.get('description')
    genres_ids = kwargs.get('genres_ids') or []
    cover_image_url = kwargs.get('cover_image_url')
    page_count = kwargs.get('page_count')
    author_name = kwargs.get('author_name')
    year = kwargs.get('year')

    book = Book(name=name, owner_id=owner_id)
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
    return book


def get_all_books():
    return session.query(Book).all()


def get_book_by_id(id):
    try:
        return session.query(Book).filter_by(id=id).one()
    except:
        return None


def is_book_liked_by_current_user(book_id):
    user_id = get_current_user_id()
    if not user_id:
        return False
    return True if get_like(book_id, user_id) else False


def update_book(book_id, **kwargs):
    book = get_book_by_id(book_id)
    if not book:
        return False
    owner_id = get_current_user_id()
    if not owner_id:
        return False
    if book.owner_id != owner_id:
        return False
    description = kwargs.get('description')
    genres_ids = kwargs.get('genres_ids') or []
    cover_image_url = kwargs.get('cover_image_url')
    page_count = kwargs.get('page_count')
    author_name = kwargs.get('author_name')
    year = kwargs.get('year')

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
    return book


def delete_book(book_id):
    book = get_book_by_id(book_id)
    if not book:
        return False
    owner_id = get_current_user_id()
    if not owner_id:
        return False
    if book.owner_id != owner_id:
        return False
    for l in book.likes:
        session.delete(l)
    session.delete(book)
    session.commit()
    return True



###########################  Genre Helper Functions  ###########################

def create_genre(name):
    current_user_id = get_current_user_id()
    if not current_user_id:
        return False
    genre = get_genre_by_name(name)
    if genre:
        return genre
    genre = Genre(name=name, owner_id=current_user_id)
    session.add(genre)
    session.commit()
    return genre


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


def edit_genre(genre_id, name):
    genre = get_genre_by_id(genre_id)
    if not genre:
        return False
    current_user_id = get_current_user_id()
    if not current_user_id:
        return False
    if genre.owner_id != current_user_id:
        return False
    if not name:
        return False
    genre.name = name
    session.add(genre)
    session.commit()
    return genre


def delete_genre(genre_id):
    genre = get_genre_by_id(genre_id)
    if not genre:
        return False
    current_user_id = get_current_user_id()
    if not current_user_id:
        return False
    if genre.owner_id != current_user_id:
        return False
    session.delete(genre)
    session.commit()
    return True



###########################  Like Helper Functions  ############################

def like_book(book_id):
    if not get_book_by_id(book_id):
        return
    current_user_id = get_current_user_id()
    if not current_user_id:
        return
    if get_like(book_id, current_user_id):
        return
    like = Like(book_id=book_id, user_id=current_user_id)
    session.add(like)
    session.commit()
    return like


def get_like(book_id, user_id):
    try:
        return session.query(Like).filter_by(book_id=book_id,
                                             user_id=user_id).one()
    except:
        return None


def dislike_book(book_id):
    if not get_book_by_id(book_id):
        return False
    current_user_id = get_current_user_id()
    if not current_user_id:
        return False
    like = get_like(book_id, current_user_id)
    if not like:
        return False
    session.delete(like)
    session.commit()
    return True
