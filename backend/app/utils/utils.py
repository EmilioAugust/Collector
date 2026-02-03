import httpx
from environs import Env
from mdclense.parser import MarkdownParser
from app.core.settings import Separators

env = Env()
env.read_env(".env")
OMDB_API_KEY = env("OMDB_API_KEY")

first_sep = Separators.first_sep
second_sep = Separators.second_sep

# SERIES

async def fetch_series_name_description(series_name: str):
    url = f'https://api.tvmaze.com/search/shows?q={series_name}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    data = response.json()
    result = []
    for d in data:
        show = d.get("show") or {}
        image = show.get("image") or {}
        result.append({
                "tvmaze_id": show.get("id"),
                "name": show.get("name"),
                "description": show.get("summary"),
                "poster": image.get("original"),
                "premiered": show.get("premiered"),
                "ended": show.get("ended"),
            })
    return result

async def fetch_series_details(tvmaze_id: str):
    url = f'https://api.tvmaze.com/shows/{tvmaze_id}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    data = response.json()
    details = {"tvmaze_id": data["id"],
               "name": data["name"],
               "description": data["summary"],
               "poster": data["image"]["original"],
               "premiered": data["premiered"],
               "ended": data["ended"],
               "imdb_rating": data["rating"]["average"]}
    return details

async def fetch_series_season_amount(tvmaze_id: str):
    url = f'https://api.tvmaze.com/shows/{tvmaze_id}/seasons'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    data = response.json()
    return len(data)

# MOVIES

async def fetch_search_movies(search: str, page: int):
    url = f'https://www.omdbapi.com/?s={search}&type=movie&page={page}&apikey={OMDB_API_KEY}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    data = response.json()
    return data

async def fetch_movie_details(imdb_id: str):
    url = f'https://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    data = response.json()
    return data

# BOOKS

async def fetch_search_books(search: str):
    url = f'https://openlibrary.org/search.json?q={search}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    data = response.json()
    result = []
    for d in data["docs"]:
        result.append({
            "author": d.get("author_name"),
            "cover": d["cover_edition_key"] if "cover_edition_key" in d else None,
            "olib_id": d["key"],
            "title": d["title"]
        })
    return result

def clean_description(raw_description: str):
    parser = MarkdownParser()
    first_stripping = raw_description.split(first_sep, 1)[0]
    markdown_stripping = parser.parse(first_stripping)
    plain_text = markdown_stripping.split(second_sep, 1)[0]
    return plain_text

async def fetch_book_details(olib_id: str, author: str, title: str, cover: str):
    url = f'https://openlibrary.org{olib_id}.json'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    data = response.json()
    if "description" in data:
        if "value" in data["description"]:
            description = data["description"]["value"]
        else:
            description = data["description"]
    else:
        description = "No description available" 
    
    datas = {"olib_id": olib_id, "author": author, "title": title, "description": clean_description(description), "cover": cover}
    return datas

async def normalize_text_for_book_cover(cover_edition_key: str):
    url = f"https://covers.openlibrary.org/b/olid/{cover_edition_key}-L.jpg"
    return url