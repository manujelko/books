from typing import Optional
from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(
        title="Description of the book", min_length=1, max_length=100
    )
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": "dbdcf240c7c4430ca8112f33989c1681",
                "title": "Computer Science Pro",
                "author": "Codingwithroby",
                "description": "A very nice description of a book",
                "rating": 75,
            }
        }


BOOKS = []


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if len(BOOKS) < 1:
        create_books_no_api()
    
    if books_to_return and 0 < books_to_return < len(BOOKS):
        return BOOKS[:books_to_return]

    return BOOKS


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book


def create_books_no_api():
    book_1 = Book(
        id="f0c99f887817423c82fda84aa5ec784b",
        title="Title 1",
        author="Author 1",
        description="Description 1",
        rating=60,
    )
    book_2 = Book(
        id="a773632ca4754793bff5af943e5bb2fc",
        title="Title 2",
        author="Author 2",
        description="Description 2",
        rating=60,
    )
    book_3 = Book(
        id="1525a9d574ee4db0b81935b6dc4d8ff1",
        title="Title 3",
        author="Author 3",
        description="Description 3",
        rating=60,
    )
    book_4 = Book(
        id="20b7ac1df44645f2b86611af2a4cf6d7",
        title="Title 4",
        author="Author 4",
        description="Description 4",
        rating=60,
    )
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
