import logging
from fastapi import FastAPI
from app.series.add_series import series_router
from app.movies.add_movies import movies_router
from app.books.add_books import books_router
from app.auth.auth import auth_router
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] #%(levelname)-4s %(filename)s:%(lineno)d - %(message)s",
                    handlers=[
                        logging.FileHandler("app/logs/app.log", encoding="utf-8"),
                        logging.StreamHandler()
                    ])

app = FastAPI(tags=['main'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://frontend:80"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(series_router)
app.include_router(movies_router)
app.include_router(books_router)

@app.get("/")
async def main():
    return {"message": "Welcome to Collector!"}