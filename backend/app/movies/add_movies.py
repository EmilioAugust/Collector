import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import Users, get_db
from app.auth.auth import get_current_user
from app.movies.movies import adding_movies, show_search_results, deleting_movies, updating_movies_status, showing_movies_status, showing_movies
from app.models.models import AddMovies
from app.celery_app.celery import show_movies_celer
from app.core.redis import r

movies_router = APIRouter(prefix='/films', tags=['films'])
CACHE_TTL = 3600

@movies_router.get("/show_search_results")
async def showing_search_results(query: str, page: int = 1, limit: int = 10, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    data = await show_search_results(query, page, current_user, db)
    return data["Search"][:limit]

@movies_router.post("/add_movies")
async def add_movies(query: AddMovies, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    #r.delete(f"usermovies:{current_user.id}")
    return await adding_movies(query, current_user=current_user.id, db=db)

@movies_router.get("/show_movies")
async def show_movies(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    # cache_key = f"usermovies:{current_user.id}"
    # cached = r.get(cache_key)
    # if cached:
    #     return json.loads(cached)
    # task = show_movies_celer.delay(current_user.id)
    # result = task.get(timeout=40)
    # r.setex(cache_key, 60 * 10, json.dumps(result))
    return showing_movies(current_user=current_user.id, db=db)

@movies_router.get("/show_movies_status")
async def show_series_status(status: str, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    return await showing_movies_status(status=status, current_user=current_user.id, db=db)

@movies_router.delete("/delete_movies")
async def delete_movies(id: int, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    #r.delete(f"usermovies:{current_user.id}")
    return await deleting_movies(id=id, current_user=current_user.id, db=db)

@movies_router.put("/update_movies_status")
async def update_series_status(id: int, status: str, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    #r.delete(f"usermovies:{current_user.id}")
    return await updating_movies_status(id, status, current_user.id, db)