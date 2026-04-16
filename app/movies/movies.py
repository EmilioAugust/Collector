import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.database import Movies, UserMovies
from app.models.models import FoundMovie, AddMovies, StatusFilter
from app.utils.utils import fetch_movie_details, fetch_search_movies

async def show_search_results(query: str, page: int, current_user: int, db: Session):
    data = await fetch_search_movies(query, page)
    if data is None:
        raise HTTPException(status_code=404, detail="Not found")
    return data

async def adding_movies(imdb_id: AddMovies, current_user: int, db: Session):
    details = await fetch_movie_details(imdb_id.imdb_id)
    movies = db.query(Movies).filter(Movies.imdb_id == imdb_id.imdb_id).first()
    if not movies:
        movies = Movies(imdb_id=details["imdbID"], name=details["Title"], description=details["Plot"], year=details["Year"], imdb_rating=details["imdbRating"], poster=details["Poster"])
        logging.info(f"New movie added to database: {movies.name}")
        db.add(movies)
        db.flush()
    else:
        logging.info("Movie taken from database")
    existing_movies_in_user = db.query(UserMovies).filter(UserMovies.user_id == current_user, UserMovies.movies_id == movies.id).first()
    if existing_movies_in_user:
        logging.info("Movie already exists in collection of user.")
        raise HTTPException(status_code=409, detail="Movie already exists in collection.")
    user_movies = UserMovies(user_id=current_user, movies_id=movies.id, status=imdb_id.status)
    db.add(user_movies)
    db.commit()
    logging.info("Movie added to user's collection.")
    return {"message": "Movie added to your collection."}

def showing_movies(current_user: int, db: Session):
    films = []
    existing_movies_in_user = db.query(UserMovies).filter(UserMovies.user_id == current_user, UserMovies.movies_id == Movies.id).all()
    for user_movies in existing_movies_in_user:
        movies_id = user_movies.movies_id
        movies = db.query(Movies).filter(Movies.id == movies_id).all()
        for m in movies:
            films.append(FoundMovie(id=m.id, name=m.name, description=m.description, year=m.year, imdb_rating=m.imdb_rating, poster=m.poster, status=user_movies.status))
    if films:
        return films
    else:
        return {"error": 404, "detail": "List of movies is empty"}
        
    
async def showing_movies_status(status: StatusFilter, current_user: int, db: Session):
    films = []
    if status == "Watched":
        existing_movies_in_user = db.query(UserMovies).filter(UserMovies.user_id == current_user, UserMovies.movies_id == Movies.id, UserMovies.status == "Watched").all()
        for user_movies in existing_movies_in_user:
            movies_id = user_movies.movies_id
            movies = db.query(Movies).filter(Movies.id == movies_id).all()
            for m in movies:
                films.append(FoundMovie(id=m.id, name=m.name, description=m.description, year=m.year, imdb_rating=m.imdb_rating, poster=m.poster, status=user_movies.status))

    elif status == "Watching":
        existing_movies_in_user = db.query(UserMovies).filter(UserMovies.user_id == current_user, UserMovies.movies_id == Movies.id, UserMovies.status == "Watching").all()
        for user_movies in existing_movies_in_user:
            movies_id = user_movies.movies_id
            movies = db.query(Movies).filter(Movies.id == movies_id).all()
            for m in movies:
                films.append(FoundMovie(id=m.id, name=m.name, description=m.description, year=m.year, imdb_rating=m.imdb_rating, poster=m.poster, status=user_movies.status))

    elif status == "Planning":
        existing_movies_in_user = db.query(UserMovies).filter(UserMovies.user_id == current_user, UserMovies.movies_id == Movies.id, UserMovies.status == "Planning").all()
        for user_movies in existing_movies_in_user:
            movies_id = user_movies.movies_id
            movies = db.query(Movies).filter(Movies.id == movies_id).all()
            for m in movies:
                films.append(FoundMovie(id=m.id, name=m.name, description=m.description, year=m.year, imdb_rating=m.imdb_rating, poster=m.poster, status=user_movies.status))
    else:
        return {"error": 404, "detail": "List of movies is empty"}
    return films

async def deleting_movies(id: int, current_user: int, db: Session):
    result = db.query(UserMovies).filter(UserMovies.user_id == current_user).all()
    if not result:
        raise HTTPException(status_code=404, detail="Couldn't find this movie")
    else:
        for movie in result:
            if movie.movies_id == id:
                db.delete(movie)
        db.commit()
    return {"message": "Movie deleted."}

async def updating_movies_status(id: int, status: str, current_user: int, db: Session):
    user_movies = db.query(UserMovies).filter(UserMovies.user_id == current_user, UserMovies.movies_id == id).first()
    if not user_movies:
        raise HTTPException(status_code=404, detail="Movie not found in your collection")
    user_movies.status = status
    try:
        db.commit()
        db.refresh(user_movies)
        return {"message": "Movie status updated successfully"}
    except Exception as e:
        db.rollback()
        return {"error": e}