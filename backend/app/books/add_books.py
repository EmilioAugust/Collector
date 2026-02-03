import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import Users, get_db
from app.auth.auth import get_current_user
from app.books.books import show_search_results_books, adding_book, deleting_books, showing_books_status, updating_books_status, showing_books
from app.models.models import AddBooks
from app.celery_app.celery import show_books_celer
from app.core.redis import r

books_router = APIRouter(prefix='/books', tags=['books'])

@books_router.get("/show_search_results_book")
async def showing_search_results_book(query: str, limit: int = 10, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    data = await show_search_results_books(query, current_user, db)
    return data[:limit]

@books_router.post("/add_books")
async def add_books(data: AddBooks, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    #r.delete(f"userbooks:{current_user.id}")
    return await adding_book(data, current_user=current_user.id, db=db)

@books_router.get("/show_books")
async def show_books(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    # cache_key = f"userbooks:{current_user.id}"
    # cached = r.get(cache_key)
    # if cached:
    #     return json.loads(cached)
    # task = show_books_celer.delay(current_user.id)
    # result = task.get(timeout=40)
    # r.setex(cache_key, 60 * 10, json.dumps(result))
    return showing_books(current_user=current_user.id, db=db)

@books_router.get("/show_books_status")
async def show_series_status(status: str, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    return await showing_books_status(status=status, current_user=current_user.id, db=db)

@books_router.delete("/delete_books")
async def delete_books(id: int, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    #r.delete(f"userbooks:{current_user.id}")
    return await deleting_books(id=id, current_user=current_user.id, db=db)

@books_router.put("/update_books_status")
async def update_series_status(id: int, status: str, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    #r.delete(f"userbooks:{current_user.id}")
    return await updating_books_status(id, status, current_user.id, db)