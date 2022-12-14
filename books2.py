from typing import Optional
from uuid import UUID

from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


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
                "id": "da9aa5f3-acf6-4528-8ef2-ac7e07b10e8d",
                "title": "Computer Science Pro",
                "author": "Codingwithroby",
                "description": "A very nice description of a book",
                "rating": 75,
            }
        }


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(
        None, title="description of the Book", max_length=100, min_length=1
    )


BOOKS = [
    Book(
        id="1ecaba70-96dd-40e9-93e8-588cee581881",
        title="Title 1",
        author="Author 1",
        description="Description 1",
        rating=60,
    ),
    Book(
        id="86367e05-58ae-4766-88ae-c8601c7ed0d6",
        title="Title 2",
        author="Author 2",
        description="Description 2",
        rating=60,
    ),
    Book(
        id="62b02aec-465d-41a4-9af8-df64a4fd65aa",
        title="Title 3",
        author="Author 3",
        description="Description 3",
        rating=60,
    ),
    Book(
        id="dc29817a-dd49-4381-95c6-dbb99d608c8f",
        title="Title 4",
        author="Author 4",
        description="Description 4",
        rating=60,
    ),
]


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(
        request: Request, exception: NegativeNumberException
):
    return JSONResponse(
        status_code=418,
        content={
            "message": f"Hey, wahy do you want {exception.books_to_return}? You need to read more"
        },
    )


@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header": random_header}


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

    if books_to_return and 0 < books_to_return < len(BOOKS):
        return BOOKS[:books_to_return]

    return BOOKS


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.post("/books/login/")
async def books_login(book_id: int, username: Optional[str] = Header(None), password: Optional[str] = Header(None)):
    if username == "FastAPIUser" and password == "test1234!":
        return BOOKS[book_id]
    return "Invalid user"


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for book in BOOKS:
        if str(book.id) == str(book_id):
            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found",
        headers={"X-Header-Error": "Nothing to be seen"},
    )


@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for book in BOOKS:
        if str(book.id) == str(book_id):
            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found",
        headers={"X-Header-Error": "Nothing to be seen"},
    )


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for i, _book in enumerate(BOOKS):
        if str(_book.id) == str(book_id):
            BOOKS[i] = book
            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found",
        headers={"X-Header-Error": "Nothing to be seen"},
    )


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    for i, book in enumerate(BOOKS):
        if str(book.id) == str(book_id):
            del BOOKS[i]
            return

    raise HTTPException(
        status_code=404,
        detail="Book not found",
        headers={"X-Header-Error": "Nothing to be seen"},
    )
