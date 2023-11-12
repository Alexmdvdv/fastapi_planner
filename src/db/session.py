from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)

engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    with session_maker() as session:
        yield session
