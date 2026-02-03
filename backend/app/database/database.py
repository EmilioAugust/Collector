import re
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Date
from environs import Env

env = Env()
env.read_env(".env")
url_database = env("URL_DB")

engine = create_engine(url_database)
Base = declarative_base()

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def is_valid_email(email):
    return re.match(EMAIL_REGEX, email) is not None

# AUTH

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user_series = relationship("UserSeries", back_populates="user", cascade="all, delete-orphan")
    user_movies = relationship("UserMovies", back_populates="user", cascade="all, delete-orphan")
    user_books = relationship("UserBooks", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, username, email, hashed_password):
        if not is_valid_email(email):
            raise ValueError("Invalid email address {email}")
        self.username = username
        self.email = email
        self.hashed_password = hashed_password

# SERIES

class Series(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True)
    tvmaze_id = Column(Integer, unique=True, index=True)
    name = Column(String)
    premiered = Column(Date)
    ended = Column(Date, nullable=True)
    description = Column(String)
    season_amount = Column(Integer)
    poster = Column(String, nullable=True)
    imdb_rating = Column(Float, nullable=True)

    user_series = relationship("UserSeries", back_populates="series", cascade="all, delete-orphan")

    def __init__(self, tvmaze_id, name, premiered, ended, description, season_amount, poster, imdb_rating):
        self.tvmaze_id = tvmaze_id
        self.name= name
        self.premiered = premiered
        self.ended = ended
        self.description = description
        self.season_amount = season_amount
        self.poster = poster
        self.imdb_rating = imdb_rating

class UserSeries(Base):
    __tablename__ = "userseries"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    series_id = Column(Integer, ForeignKey("series.id"))
    status = Column(String)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("Users", back_populates="user_series")
    series = relationship("Series", back_populates="user_series")

    def __init__(self, user_id, series_id, status):
        self.user_id = user_id
        self.series_id = series_id
        self.status = status

# MOVIES

class Movies(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    imdb_id = Column(String, unique=True, index=True)
    name = Column(String)
    description = Column(String)
    year = Column(Integer, nullable=True)
    imdb_rating = Column(Float, nullable=True)
    poster = Column(String, nullable=True)

    user_movies = relationship("UserMovies", back_populates="movies", cascade="all, delete-orphan")

    def __init__(self, imdb_id, name, description, year, imdb_rating, poster):
        self.imdb_id = imdb_id
        self.name= name
        self.description = description
        self.year = year
        self.imdb_rating = imdb_rating
        self.poster = poster

class UserMovies(Base):
    __tablename__ = "usermovies"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movies_id = Column(Integer, ForeignKey("movies.id"))
    status = Column(String)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("Users", back_populates="user_movies")
    movies = relationship("Movies", back_populates="user_movies")

    def __init__(self, user_id, movies_id, status):
        self.user_id = user_id
        self.movies_id = movies_id
        self.status = status

# BOOKS

class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    olib_id = Column(String, unique=True, index=True, nullable=True)
    author = Column(String, nullable=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    cover = Column(String, nullable=True)

    user_books = relationship("UserBooks", back_populates="books", cascade="all, delete-orphan")

    def __init__(self, olib_id, author, title, description, cover):
        self.olib_id = olib_id
        self.author = author
        self.title = title
        self.description = description
        self.cover = cover

class UserBooks(Base):
    __tablename__ = "userbooks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    books_id = Column(Integer, ForeignKey("books.id"))
    status = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("Users", back_populates="user_books")
    books = relationship("Books", back_populates="user_books")

    def __init__(self, user_id, books_id, status):
        self.user_id = user_id
        self.books_id = books_id
        self.status = status

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()