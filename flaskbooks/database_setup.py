from sqlalchemy import create_engine
from sqlalchemy_utils.functions import database_exists, drop_database

from model import Base, db_name

if __name__ == '__main__':

    # Drop old database if exists
    if database_exists(db_name):
        drop_database(db_name)

    # Create engine
    engine = create_engine(db_name)
    Base.metadata.create_all(engine)

    print("Database created!")
