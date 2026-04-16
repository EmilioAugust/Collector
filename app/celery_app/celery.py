from celery import Celery
from app.config.config import Config
from app.movies.movies import showing_movies
from app.series.series import showing_series
from app.books.books import showing_books
from fastapi.encoders import jsonable_encoder
from app.database.database import SessionLocal

celery = Celery('collector')
celery.config_from_object(Config)

@celery.task
def show_books_celer(user_id: int):
    db = SessionLocal()
    try:
        result = showing_books(current_user=user_id, db=db)
        return jsonable_encoder(result)
    finally:
        db.close()

@celery.task
def show_movies_celer(user_id: int):
    db = SessionLocal()
    try:
        result = showing_movies(current_user=user_id, db=db)
        return jsonable_encoder(result)
    finally:
        db.close()

@celery.task
def show_series_celer(user_id: int):
    db = SessionLocal()
    try:
        result = showing_series(current_user=user_id, db=db)
        return jsonable_encoder(result)
    finally:
        db.close()