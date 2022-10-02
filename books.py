from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

BOOKS = {
    "book_1": {"title": "Title One", "author": "Author One"},
    "book_2": {"title": "Title Two", "author": "Author Two"},
    "book_3": {"title": "Title Three", "author": "Author Three"},
    "book_4": {"title": "Title Four", "author": "Author Four"},
    "book_5": {"title": "Title Five", "author": "Author Five"},
}


@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        return [book for book in BOOKS if book != skip_book]
    return BOOKS


@app.get("/{book_name}")
async def read_book(book_name: str):
    return BOOKS[book_name]
