from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Genre, Book

engine = create_engine('sqlite:///bookstore.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

session.query(User).delete()
session.query(Genre).delete()
session.query(Book).delete()
session.commit()

user1 = User(first_name="Omar", last_name="Albeik", email="omaralbeik@gmail.com")
user2 = User(first_name="Jane", last_name="Doe", email="jane.doe@gmail.com")
user3 = User(first_name="John", last_name="Applesead", email="john.applesead@apple.com")
users = [user1, user2, user3]
for u in users:
    session.add(u)
session.commit()

genre1 = Genre(name="Non Fiction", user_id=1)
genre2 = Genre(name="Fiction", user_id=1)
genre3 = Genre(name="Mystery", user_id=1)
genre4 = Genre(name="Horror", user_id=1)
genre5 = Genre(name="Poetry", user_id=2)
genre6 = Genre(name="Diaries", user_id=2)
genre7 = Genre(name="Series", user_id=3)
genre8 = Genre(name="Biographies", user_id=3)


genres = [genre1, genre2, genre3, genre4, genre5, genre6, genre7, genre8]
for g in genres:
    session.add(g)
session.commit()

book1 = Book(name='Silent Spring', description="Silent Spring is an environmental science book by Rachel Carson. The book was published on 27 September 1962 and it documented the detrimental effects on the environment of the indiscriminate use of pesticides.", author_name="Rachel Carson", pages_count = 264, year=2004, price=8.95, genre_id=1, user_id=1, cover_image_url="https://images.gr-assets.com/books/1442353674l/27333.jpg")

book2 = Book(name="The Handmaid's Tale", description="The Handmaid's Tale is set in the Republic of Gilead, a theocratic military dictatorship formed within the borders of what was formerly the United States of America. ... Offred describes the structure of Gilead's society, including the several different classes of women and their circumscribed lives in the new theocracy.", author_name="Margaret Atwood", year=1985, price=9.81, genre_id=2, user_id=2, cover_image_url="https://images.gr-assets.com/books/1498057733l/38447.jpg")

book3 = Book(name="Ender's Game", description="Ender's Game is a 1985 military science fiction novel by American author Orson Scott Card. Set in Earth's future, the novel presents an imperiled mankind after two conflicts with the \"buggers\", an insectoid alien species.", pages_count = 420, author_name="Orson Scott Card", year=1985, price=12.81, genre_id=2, user_id=3, cover_image_url="https://images.gr-assets.com/books/1408303130l/375802.jpg")

book4 = Book(name="Bossypants", description="Before Liz Lemon, before \"Weekend Update,\" before \"Sarah Palin,\" Tina Fey was just a young girl with a dream: a recurring stress dream that she was being chased through a local airport by her middle-school gym teacher. She also had a dream that one day she would be a comedian on TV.", pages_count = 283, author_name="Tina Fey", year=2011, genre_id=1, user_id=3, cover_image_url="https://images.gr-assets.com/books/1481509554l/9418327.jpg")

book5 = Book(name="Elon Musk: Tesla, SpaceX, and the Quest for a Fantastic Future", description="Elon Musk: Tesla, SpaceX, and the Quest for a Fantastic Future is Ashlee Vance's biography of Elon Musk, published in 2015.", pages_count = 400, author_name="Ashlee Vance", year=2015, genre_id=8, user_id=2, cover_image_url="https://images.gr-assets.com/books/1404411386l/22543496.jpg")

book6 = Book(name="And Then There Were None", pages_count = 283, author_name="Agatha Christie", year=1939, genre_id=3, user_id=3, cover_image_url="https://images.gr-assets.com/books/1391120695l/16299.jpg")

books = [book1, book2, book3, book4, book5, book6]
for b in books:
    session.add(b)
session.commit()

print("Added lots of books!")
