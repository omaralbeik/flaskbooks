from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, User, Book, Genre, Like, db_name

engine = create_engine(db_name)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

session.query(User).delete()
session.query(Genre).delete()
session.query(Book).delete()
session.commit()

users = [
    User(name="Omar Albeik", email="omaralbeik@gmail.com", bio="I\’m a passionate software developer, AI enthusiast and lifelong learner!"),
    User(name="Jane Doe", email="jane.doe@gmail.com"),
    User(name="John Applesead", email="john.applesead@apple.com")
]

session.add_all(users)
session.commit()

genre1 = Genre(name="Non Fiction", owner_id=1)
genre2 = Genre(name="Fiction", owner_id=1)
genre3 = Genre(name="Mystery", owner_id=1)
genre4 = Genre(name="Horror", owner_id=2)
genre5 = Genre(name="Poetry", owner_id=2)
genre6 = Genre(name="Diaries", owner_id=3)
genre7 = Genre(name="Series", owner_id=3)
genre8 = Genre(name="Biographies", owner_id=3)

genres = [genre1, genre2, genre3, genre4, genre5, genre6, genre7, genre8]

session.add_all(genres)
session.commit()

book1 = Book(name='Silent Spring',
             description="Silent Spring is an environmental science book by Rachel Carson. The book was published on 27 September 1962 and it documented the detrimental effects on the environment of the indiscriminate use of pesticides.",
             cover_image_url="https://images.gr-assets.com/books/1442353674l/27333.jpg",
             page_count = 264,
             author_name="Rachel Carson",
             year=2004,
             owner_id=1)

book1.genres.append(genre1)
book1.genres.append(genre2)

book2 = Book(name="The Handmaid's Tale",
             description="The Handmaid's Tale is set in the Republic of Gilead, a theocratic military dictatorship formed within the borders of what was formerly the United States of America. ... Offred describes the structure of Gilead's society, including the several different classes of women and their circumscribed lives in the new theocracy.",
             cover_image_url="https://images.gr-assets.com/books/1498057733l/38447.jpg",
             author_name="Margaret Atwood",
             year=1985,
             owner_id=1)

book2.genres.append(genre4)
book2.genres.append(genre5)

book3 = Book(name="Ender's Game",
             description="Ender's Game is a 1985 military science fiction novel by American author Orson Scott Card. Set in Earth's future, the novel presents an imperiled mankind after two conflicts with the \"buggers\", an insectoid alien species.",
             cover_image_url="https://images.gr-assets.com/books/1408303130l/375802.jpg",
             page_count = 420,
             author_name="Orson Scott Card",
             year=1985,
             owner_id=2)

book3.genres.append(genre4)
book3.genres.append(genre3)
book3.genres.append(genre5)
book3.genres.append(genre6)

book4 = Book(name="Bossypants",
             description="Before Liz Lemon, before \"Weekend Update,\" before \"Sarah Palin,\" Tina Fey was just a young girl with a dream: a recurring stress dream that she was being chased through a local airport by her middle-school gym teacher. She also had a dream that one day she would be a comedian on TV.",
             cover_image_url="https://images.gr-assets.com/books/1481509554l/9418327.jpg",
             page_count = 283,
             author_name="Tina Fey",
             year=2011,
             owner_id=3)

book4.genres.append(genre2)

book5 = Book(name="Elon Musk: Tesla, SpaceX, and the Quest for a Fantastic Future",
             description="Elon Musk: Tesla, SpaceX, and the Quest for a Fantastic Future is Ashlee Vance's biography of Elon Musk, published in 2015.",
             cover_image_url="https://images.gr-assets.com/books/1404411386l/22543496.jpg",
             page_count = 400,
             author_name="Ashlee Vance",
             year=2015,
             owner_id=1)

book6 = Book(name="And Then There Were None",
             cover_image_url="https://images.gr-assets.com/books/1391120695l/16299.jpg",
             page_count = 283,
             author_name="Agatha Christie",
             year=1939,
             owner_id=3)

book6.genres.append(genre1)
book6.genres.append(genre2)
book6.genres.append(genre6)

books = [book1, book2, book3, book4, book5, book6]

session.add_all(books)
session.commit()

print("Added lots of books!")
