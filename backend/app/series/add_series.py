import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import Users, get_db
from app.auth.auth import get_current_user
from app.celery_app.celery import show_series_celer
from app.models.models import AddSeries
from app.series.series import adding_series, deleting_series, show_search_results_series, showing_series_status, updating_series_status, showing_series
from app.core.redis import r

series_router = APIRouter(prefix='/tv_shows', tags=['tv_shows'])
CACHE_TTL = 3600

@series_router.get("/show_search_results")
async def showing_search_results(query: str, limit: int = 10, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    data = await show_search_results_series(query, current_user, db)
    return data[:limit]

@series_router.post("/add_series")
async def add_series(tvmaze_id: AddSeries, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    #r.delete(f"userseries:{current_user.id}")
    return await adding_series(tvmaze_id, current_user=current_user.id, db=db)

@series_router.get("/show_series")
async def show_series(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    # cache_key = f"userseries:{current_user.id}"
    # cached = r.get(cache_key)
    # if cached:
    #     return json.loads(cached)
    # task = show_series_celer.delay(current_user.id)
    # result = task.get(timeout=40)
    # r.setex(cache_key, 60 * 10, json.dumps(result, default=str))
    return showing_series(current_user=current_user.id, db=db)

@series_router.get("/show_series_status")
async def show_series_status(status: str, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    return await showing_series_status(status=status, current_user=current_user.id, db=db)

@series_router.delete("/delete_series")
async def delete_series(id: int, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    #r.delete(f"userseries:{current_user.id}")
    return await deleting_series(id=id, current_user=current_user.id, db=db)

@series_router.put("/update_series_status")
async def update_series_status(id: int, status: str, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    #r.delete(f"userseries:{current_user.id}")
    return await updating_series_status(id, status, current_user.id, db)