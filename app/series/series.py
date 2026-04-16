import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.database import Series, UserSeries
from app.models.models import FoundSerial, AddSeries, StatusFilter
from app.utils.utils import fetch_series_name_description, fetch_series_season_amount, fetch_series_details

async def show_search_results_series(query: str, current_user: int, db: Session):
    data = await fetch_series_name_description(query)
    return data

async def adding_series(tvmaze_id: AddSeries, current_user: int, db: Session):    
    data = await fetch_series_details(tvmaze_id.tvmaze_id)
    seasons = await fetch_series_season_amount(tvmaze_id.tvmaze_id)
    series = db.query(Series).filter(Series.tvmaze_id == data.get("tvmaze_id")).first()
    if not series:
        series = Series(tvmaze_id=data.get("tvmaze_id"), name=data.get("name"), premiered=data.get("premiered"), ended=data.get("ended"),
                        description=data.get("description"), season_amount=seasons, poster=data.get("poster"), imdb_rating=data.get("imdb_rating"))
        logging.info(f"New series added to database: {series.name}")
        db.add(series)
        db.flush()
    else:
        logging.info("Series taken from database")
    existing_series_in_user = db.query(UserSeries).filter(UserSeries.user_id == current_user, UserSeries.series_id == series.id).first()
    if existing_series_in_user:
        logging.info(f"Series already exists in collection of user.")
        raise HTTPException(status_code=409, detail="Series already exists in collection.")
    user_series = UserSeries(user_id=current_user, series_id=series.id, status=tvmaze_id.status)
    db.add(user_series)
    db.commit()
    logging.info("Series added to user's collection.")
    return {"message": "Series added to your collection."}

def showing_series(current_user: int, db: Session):
    shows = []
    existing_series_in_user = db.query(UserSeries).filter(UserSeries.user_id == current_user, UserSeries.series_id == Series.id).all()
    for user_series in existing_series_in_user:
        series_id = user_series.series_id
        series = db.query(Series).filter(Series.id == series_id).all()
        for s in series:
            shows.append(FoundSerial(id=s.id, name=s.name, premiered=s.premiered, ended=s.ended,
                                     description=s.description, season_amount=s.season_amount, poster=s.poster, imdb_rating=s.imdb_rating, status=user_series.status))
    if shows:
        return shows
    else:
        return {"error": 404, "detail": "List of series is empty"}

async def showing_series_status(status: StatusFilter, current_user: int, db: Session):
    shows = []
    if status == "Watched":
        existing_series_in_user = db.query(UserSeries).filter(UserSeries.user_id == current_user, UserSeries.series_id == Series.id, UserSeries.status == "Watched").all()
        for user_series in existing_series_in_user:
            series_id = user_series.series_id
            series = db.query(Series).filter(Series.id == series_id).all()
            for s in series:
                found_serial = FoundSerial(id=s.id, name=s.name, premiered=s.premiered, ended=s.ended,
                                           description=s.description, season_amount=s.season_amount, poster=s.poster, imdb_rating=s.imdb_rating, status=user_series.status)
                shows.append(found_serial)
    elif status == "Watching":
        existing_series_in_user = db.query(UserSeries).filter(UserSeries.user_id == current_user, UserSeries.series_id == Series.id, UserSeries.status == "Watching").all()
        for user_series in existing_series_in_user:
            series_id = user_series.series_id
            series = db.query(Series).filter(Series.id == series_id).all()
            for s in series:
                found_serial = FoundSerial(id=s.id, name=s.name, premiered=s.premiered, ended=s.ended,
                                           description=s.description, season_amount=s.season_amount, poster=s.poster, imdb_rating=s.imdb_rating, status=user_series.status)
                shows.append(found_serial)
    elif status == "Planning":
        existing_series_in_user = db.query(UserSeries).filter(UserSeries.user_id == current_user, UserSeries.series_id == Series.id, UserSeries.status == "Planning").all()
        for user_series in existing_series_in_user:
            series_id = user_series.series_id
            series = db.query(Series).filter(Series.id == series_id).all()
            for s in series:
                found_serial = FoundSerial(id=s.id, name=s.name, premiered=s.premiered, ended=s.ended,
                                           description=s.description, season_amount=s.season_amount, poster=s.poster, imdb_rating=s.imdb_rating, status=user_series.status)
                shows.append(found_serial)
    elif status != StatusFilter or not shows:
        return {"message": "Series with status you entered not found"}
    else:
        return {"message": "List of series is empty"}
    return shows

async def deleting_series(id: int, current_user: int, db: Session):
    result = db.query(UserSeries).filter(UserSeries.user_id == current_user).all()
    if not result:
        raise HTTPException(status_code=404, detail="Couldn't find this series")
    else:
        for series in result:
            if series.series_id == id:
                db.delete(series)
        db.commit()
    return {"message": "Series deleted."}

async def updating_series_status(id: int, status: str, current_user: int, db: Session):
    user_series = db.query(UserSeries).filter(UserSeries.user_id == current_user, UserSeries.series_id == id).first()
    if not user_series:
        raise HTTPException(status_code=404, detail="Series not found in your collection")
    user_series.status = status
    try:
        db.commit()
        db.refresh(user_series)
        return {"message": "Series status updated successfully"}
    except Exception as e:
        db.rollback()
        return {"error": e}