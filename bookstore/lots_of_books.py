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

user1 = User(id=1, name="Omar Albeik", email="omaralbeik@gmail.com")
user2 = User(id=2, name="Mert Akengin", email="mert.akengin@gmail.com")
user3 = User(id=3, name="John Applesead", email="john.applesead@apple.com")
users = [user1, user2, user3]
for u in users:
    session.add(u)
session.commit()

genre1 = Genre(id=1, name="Non Fiction", user_id=1)
genre2 = Genre(id=2, name="Fiction", user_id=2)
genres = [genre1, genre2]
for g in genres:
    session.add(g)
session.commit()

book1 = Book(id=1, name='Silent Spring', description="Silent Spring is an environmental science book by Rachel Carson. The book was published on 27 September 1962 and it documented the detrimental effects on the environment of the indiscriminate use of pesticides.", author_name="Rachel Carson", pages_count = 264, year=2004, price=8.95, genre_id=1, user_id=1)

book2 = Book(id=2, name="The Handmaid's Tale", description="The Handmaid's Tale is set in the Republic of Gilead, a theocratic military dictatorship formed within the borders of what was formerly the United States of America. ... Offred describes the structure of Gilead's society, including the several different classes of women and their circumscribed lives in the new theocracy.", author_name="Margaret Atwood", year=1985, price=9.81, genre_id=2, user_id=2)

book3 = Book(id=3, name="Ender's Game", description="Ender's Game is a 1985 military science fiction novel by American author Orson Scott Card. Set in Earth's future, the novel presents an imperiled mankind after two conflicts with the \"buggers\", an insectoid alien species.", pages_count = 420, author_name="Orson Scott Card", year=1985, price=12.81, genre_id=2, user_id=3)
books = [book1, book2, book3]
for b in books:
    session.add(b)
session.commit()

print("Added lots of books!")
