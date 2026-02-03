import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.database import Books, UserBooks
from app.models.models import FoundBook, AddBooks, StatusFilterBook
from app.utils.utils import fetch_search_books, fetch_book_details

async def show_search_results_books(query: str, current_user: int, db: Session):
    data = await fetch_search_books(query)
    return data

async def adding_book(data: AddBooks, current_user: int, db: Session):
    details = await fetch_book_details(olib_id=data.olib_id, author=data.author, title=data.title, cover=data.cover)
    books = db.query(Books).filter(Books.olib_id == data.olib_id).first()
    if not books:
        books = Books(olib_id=details.get("olib_id"), author=details.get("author"), title=details.get("title"), description=details.get("description"), cover=details.get("cover"))
        logging.info(f"New book added to database: {books.title}")
        db.add(books)
        db.flush()
    else:
        logging.info("Book taken from database")
    existing_books_in_user = db.query(UserBooks).filter(UserBooks.user_id == current_user, UserBooks.books_id == books.id).first()
    if existing_books_in_user:
        logging.info("Book already exists in collection of user.")
        raise HTTPException(status_code=409, detail="Book already exists in collection.")
    user_books = UserBooks(user_id=current_user, books_id=books.id, status=data.status)
    db.add(user_books)
    db.commit()
    logging.info("Book added to user's collection.")
    return {"message": "Book added to your collection."}

def showing_books(current_user: int, db: Session):
    all_books = []
    existing_books_in_user = db.query(UserBooks).filter(UserBooks.user_id == current_user, UserBooks.books_id == Books.id).all()
    for user_books in existing_books_in_user:
        books_id = user_books.books_id
        books = db.query(Books).filter(Books.id == books_id).all()
        for b in books:
            all_books.append(FoundBook(id=b.id, author=b.author, title=b.title, description=b.description, cover=b.cover, status=user_books.status))
    if all_books:
        return all_books
    else:
        return {"error": 404, "detail": "List of books is empty"}
    
async def showing_books_status(status: StatusFilterBook, current_user: int, db: Session):
    all_books = []
    if status == "Read":
        existing_books_in_user = db.query(UserBooks).filter(UserBooks.user_id == current_user, UserBooks.books_id == Books.id, UserBooks.status == "Read").all()
        for user_books in existing_books_in_user:
            books_id = user_books.books_id
            books = db.query(Books).filter(Books.id == books_id).all()
            for b in books:
                all_books.append(FoundBook(id=b.id, author=b.author, title=b.title, description=b.description, cover=b.cover, status=user_books.status))

    elif status == "Reading":
        existing_books_in_user = db.query(UserBooks).filter(UserBooks.user_id == current_user, UserBooks.books_id == Books.id, UserBooks.status == "Reading").all()
        for user_books in existing_books_in_user:
            books_id = user_books.books_id
            books = db.query(Books).filter(Books.id == books_id).all()
            for b in books:
                all_books.append(FoundBook(id=b.id, author=b.author, title=b.title, description=b.description, cover=b.cover, status=user_books.status))

    elif status == "Planning":
        existing_books_in_user = db.query(UserBooks).filter(UserBooks.user_id == current_user, UserBooks.books_id == Books.id, UserBooks.status == "Planning").all()
        for user_books in existing_books_in_user:
            books_id = user_books.books_id
            books = db.query(Books).filter(Books.id == books_id).all()
            for b in books:
                all_books.append(FoundBook(id=b.id, author=b.author, title=b.title, description=b.description, cover=b.cover, status=user_books.status))
    else:
        return {"error": 404, "detail": "List of movies is empty"}
    return all_books

async def deleting_books(id: int, current_user: int, db: Session):
    result = db.query(UserBooks).filter(UserBooks.user_id == current_user).all()
    if not result:
        raise HTTPException(status_code=404, detail="Couldn't find book")
    else:
        for book in result:
            if book.books_id == id:
                db.delete(book)
        db.commit()
    return {"message": "Book deleted."}

async def updating_books_status(id: int, status: str, current_user: int, db: Session):
    user_series = db.query(UserBooks).filter(UserBooks.user_id == current_user, UserBooks.books_id == id).first()
    if not user_series:
        raise HTTPException(status_code=404, detail="Book not found in your collection")
    user_series.status = status
    try:
        db.commit()
        db.refresh(user_series)
        return {"message": "Book status updated successfully"}
    except Exception as e:
        db.rollback()
        return {"error": e}