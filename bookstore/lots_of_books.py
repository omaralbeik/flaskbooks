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

user1 = User(name="Omar Albeik", email="omaralbeik@gmail.com")
user2 = User(name="Mert Akengin", email="mert.akengin@gmail.com")
user3 = User(name="John Applesead", email="john.applesead@apple.com")
users = [user1, user2, user3]
for u in users:
    session.add(u)
session.commit()

genre1 = Genre(name="Non Fiction", user_id=1)
genre2 = Genre(name="Fiction", user_id=2)
genres = [genre1, genre2]
for g in genres:
    session.add(g)
session.commit()

book1 = Book(name='Silent Spring', description="Silent Spring is an environmental science book by Rachel Carson. The book was published on 27 September 1962 and it documented the detrimental effects on the environment of the indiscriminate use of pesticides.", author_name="Rachel Carson", pages_count = 264, year=2004, price=8.95, genre_id=1, user_id=1, cover_image_url="https://images.gr-assets.com/books/1442353674l/27333.jpg")

book2 = Book(name="The Handmaid's Tale", description="The Handmaid's Tale is set in the Republic of Gilead, a theocratic military dictatorship formed within the borders of what was formerly the United States of America. ... Offred describes the structure of Gilead's society, including the several different classes of women and their circumscribed lives in the new theocracy.", author_name="Margaret Atwood", year=1985, price=9.81, genre_id=2, user_id=2, cover_image_url="https://images.gr-assets.com/books/1498057733l/38447.jpg")

book3 = Book(name="Ender's Game", description="Ender's Game is a 1985 military science fiction novel by American author Orson Scott Card. Set in Earth's future, the novel presents an imperiled mankind after two conflicts with the \"buggers\", an insectoid alien species.", pages_count = 420, author_name="Orson Scott Card", year=1985, price=12.81, genre_id=2, user_id=3, cover_image_url="https://images.gr-assets.com/books/1408303130l/375802.jpg")

book4 = Book(name="Bossypants", description="Before Liz Lemon, before \"Weekend Update,\" before \"Sarah Palin,\" Tina Fey was just a young girl with a dream: a recurring stress dream that she was being chased through a local airport by her middle-school gym teacher. She also had a dream that one day she would be a comedian on TV.", pages_count = 283, author_name="Tina Fey", year=2011, genre_id=1, user_id=3, cover_image_url="https://images.gr-assets.com/books/1481509554l/9418327.jpg")

books = [book1, book2, book3, book4]
for b in books:
    session.add(b)
session.commit()

print("Added lots of books!")
