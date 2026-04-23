"""
Limkokwing University Library Management API
PROG315 - Object-Oriented Programming 2
Author: [Your Name]
Student ID: [Your Student ID]
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
import asyncio
from datetime import date, timedelta

# ─────────────────────────────────────────────
# App Initialization
# ─────────────────────────────────────────────
app = FastAPI(
    title="Limkokwing Library API",
    description="A RESTful API for managing the Limkokwing University Sierra Leone Library System.",
    version="1.0.0",
)

# ─────────────────────────────────────────────
# In-Memory Data Store (simulates a database)
# ─────────────────────────────────────────────
books_db: dict[int, dict] = {
    1: {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "category": "Programming", "available": True},
    2: {"id": 2, "title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "category": "Computer Science", "available": True},
    3: {"id": 3, "title": "Design Patterns", "author": "Gang of Four", "category": "Software Engineering", "available": False},
    4: {"id": 4, "title": "Python Crash Course", "author": "Eric Matthes", "category": "Programming", "available": True},
    5: {"id": 5, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "category": "Software Engineering", "available": True},
}

borrows_db: dict[int, dict] = {
    1: {
        "borrow_id": 1,
        "user_id": 101,
        "book_id": 3,
        "borrow_date": str(date.today() - timedelta(days=20)),
        "due_date": str(date.today() - timedelta(days=6)),
        "returned": False,
    }
}

users_db: dict[int, dict] = {
    101: {"user_id": 101, "name": "Aminata Kamara", "email": "aminata@limkokwing.edu.sl"},
    102: {"user_id": 102, "name": "Ibrahim Sesay", "email": "ibrahim@limkokwing.edu.sl"},
}

next_borrow_id: int = 2

# ─────────────────────────────────────────────
# Pydantic Models (Type Annotations)
# ─────────────────────────────────────────────
class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str
    available: bool

class BorrowRequest(BaseModel):
    user_id: int = Field(..., example=101, description="The ID of the user borrowing the book")
    book_id: int = Field(..., example=2, description="The ID of the book to borrow")

class ReturnRequest(BaseModel):
    borrow_id: int = Field(..., example=1, description="The borrow transaction ID to close")

class BorrowRecord(BaseModel):
    borrow_id: int
    user_id: int
    book_id: int
    borrow_date: str
    due_date: str
    returned: bool

class OverdueReport(BaseModel):
    borrow_id: int
    user_id: int
    book_id: int
    book_title: str
    days_overdue: int
    fine_usd: float

# ─────────────────────────────────────────────
# ENDPOINT 1: GET /books — Search for Books
# ─────────────────────────────────────────────
@app.get("/books", response_model=list[Book], summary="Search for books")
async def get_books(
    title: Optional[str] = Query(None, description="Filter by book title (partial match)"),
    author: Optional[str] = Query(None, description="Filter by author name (partial match)"),
    category: Optional[str] = Query(None, description="Filter by category"),
) -> list[Book]:
    """
    Search the library catalogue by title, author, or category.
    Returns a list of matching books with their availability status.
    All query parameters are optional and support partial matching.
    """
    results: list[dict] = list(books_db.values())

    if title:
        results = [b for b in results if title.lower() in b["title"].lower()]
    if author:
        results = [b for b in results if author.lower() in b["author"].lower()]
    if category:
        results = [b for b in results if category.lower() in b["category"].lower()]

    return results


# ─────────────────────────────────────────────
# ENDPOINT 2: POST /borrow — Borrow a Book
# ─────────────────────────────────────────────
@app.post("/borrow", response_model=BorrowRecord, summary="Borrow a book")
async def borrow_book(request: BorrowRequest) -> BorrowRecord:
    """
    Allows a registered user to borrow an available book.
    Marks the book as unavailable and creates a borrow record
    with a due date set to 14 days from today.
    """
    global next_borrow_id

    # Validate user
    if request.user_id not in users_db:
        raise HTTPException(status_code=404, detail=f"User with ID {request.user_id} not found.")

    # Validate book
    if request.book_id not in books_db:
        raise HTTPException(status_code=404, detail=f"Book with ID {request.book_id} not found.")

    book = books_db[request.book_id]

    if not book["available"]:
        raise HTTPException(status_code=400, detail=f"Book '{book['title']}' is currently not available.")

    # Simulate async I/O delay (e.g., writing to a database)
    await asyncio.sleep(0.05)

    # Create borrow record
    borrow_date: date = date.today()
    due_date: date = borrow_date + timedelta(days=14)

    record: dict = {
        "borrow_id": next_borrow_id,
        "user_id": request.user_id,
        "book_id": request.book_id,
        "borrow_date": str(borrow_date),
        "due_date": str(due_date),
        "returned": False,
    }

    borrows_db[next_borrow_id] = record
    books_db[request.book_id]["available"] = False
    next_borrow_id += 1

    return record


# ─────────────────────────────────────────────
# ENDPOINT 3: PUT /return/{borrow_id} — Return a Book
# ─────────────────────────────────────────────
@app.put("/return/{borrow_id}", response_model=dict, summary="Return a borrowed book")
async def return_book(borrow_id: int) -> dict:
    """
    Processes the return of a borrowed book.
    Marks the book as available again and closes the borrow record.
    Returns a confirmation message including any overdue fine owed.
    """
    if borrow_id not in borrows_db:
        raise HTTPException(status_code=404, detail=f"Borrow record {borrow_id} not found.")

    record = borrows_db[borrow_id]

    if record["returned"]:
        raise HTTPException(status_code=400, detail="This book has already been returned.")

    # Simulate async I/O delay
    await asyncio.sleep(0.05)

    due_date: date = date.fromisoformat(record["due_date"])
    today: date = date.today()
    fine: float = 0.0

    if today > due_date:
        overdue_days: int = (today - due_date).days
        fine = round(overdue_days * 0.50, 2)  # $0.50 per day

    # Update records
    record["returned"] = True
    books_db[record["book_id"]]["available"] = True

    return {
        "message": "Book returned successfully.",
        "borrow_id": borrow_id,
        "fine_owed_usd": fine,
    }


# ─────────────────────────────────────────────
# ENDPOINT 4: GET /overdue — Track Overdue Books
# ─────────────────────────────────────────────
@app.get("/overdue", response_model=list[OverdueReport], summary="Get overdue books and fines")
async def get_overdue_books() -> list[OverdueReport]:
    """
    Returns a list of all books currently overdue (not yet returned
    and past their due date). Calculates the accumulated fine for
    each record at a rate of $0.50 per overdue day.
    """
    today: date = date.today()
    overdue_list: list[OverdueReport] = []

    for record in borrows_db.values():
        if record["returned"]:
            continue

        due_date: date = date.fromisoformat(record["due_date"])

        if today > due_date:
            days_overdue: int = (today - due_date).days
            fine: float = round(days_overdue * 0.50, 2)
            book_title: str = books_db[record["book_id"]]["title"]

            overdue_list.append(
                OverdueReport(
                    borrow_id=record["borrow_id"],
                    user_id=record["user_id"],
                    book_id=record["book_id"],
                    book_title=book_title,
                    days_overdue=days_overdue,
                    fine_usd=fine,
                )
            )

    return overdue_list


# ─────────────────────────────────────────────
# ENDPOINT 5: GET /books/{book_id} — Get Book Details
# ─────────────────────────────────────────────
@app.get("/books/{book_id}", response_model=Book, summary="Get details of a specific book")
async def get_book_by_id(book_id: int) -> Book:
    """
    Retrieves full details for a single book by its unique ID.
    Useful for checking whether a specific book is currently available.
    """
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} was not found.")

    return books_db[book_id]


# ─────────────────────────────────────────────
# Async Simulation: Multiple Users Borrowing Simultaneously
# ─────────────────────────────────────────────
async def simulate_user_action(user_id: int, book_id: int, action: str) -> str:
    """Simulates a user borrowing or returning a book asynchronously."""
    await asyncio.sleep(0.1)  # Simulates network/database latency

    if action == "borrow":
        if book_id in books_db and books_db[book_id]["available"]:
            books_db[book_id]["available"] = False
            return f"User {user_id} successfully borrowed book ID {book_id}."
        else:
            return f"User {user_id} could NOT borrow book ID {book_id} — unavailable."

    elif action == "return":
        for rec in borrows_db.values():
            if rec["user_id"] == user_id and rec["book_id"] == book_id and not rec["returned"]:
                rec["returned"] = True
                books_db[book_id]["available"] = True
                return f"User {user_id} successfully returned book ID {book_id}."
        return f"User {user_id} has no active borrow for book ID {book_id}."

    return "Unknown action."


async def run_concurrent_simulation() -> None:
    """
    Demonstrates asynchronous concurrency:
    Multiple users interact with the library system at the same time.
    """
    print("\n===== Concurrent User Simulation =====")
    tasks = [
        simulate_user_action(101, 1, "borrow"),
        simulate_user_action(102, 4, "borrow"),
        simulate_user_action(101, 1, "return"),
        simulate_user_action(102, 5, "borrow"),
    ]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)
    print("======================================\n")


# ─────────────────────────────────────────────
# Run simulation on startup (for demo purposes)
# ─────────────────────────────────────────────
@app.on_event("startup")
async def startup_event() -> None:
    await run_concurrent_simulation()


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
