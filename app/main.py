from fastapi import FastAPI, Depends, HTTPException, Request
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

from app.database import SessionLocal, settings
from app import models, schemas


app = FastAPI(title="Bookstore API")

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


def require_session(request: Request):
    if "user" not in request.session:
        raise HTTPException(status_code=401, detail="Authentication required")

    return request.session["user"]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/login", tags=["Authentication"])
def login(login_data: schemas.LoginRequest, request: Request):
    if login_data.username != "admin" or login_data.password != "admin123":
        raise HTTPException(status_code=401, detail="Invalid username or password")

    request.session["user"] = login_data.username

    return {"message": "Login successful"}


@app.post("/authors", response_model=schemas.AuthorResponse, tags=["Authors"])
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_session),
):
    new_author = models.Author(name=author.name, email=author.email)

    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author


@app.get("/authors", response_model=list[schemas.AuthorResponse], tags=["Authors"])
def get_authors(db: Session = Depends(get_db)):
    return db.query(models.Author).all()


@app.get(
    "/authors/{author_id}", response_model=schemas.AuthorResponse, tags=["Authors"]
)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.put(
    "/authors/{author_id}", response_model=schemas.AuthorResponse, tags=["Authors"]
)
def update_author(
    author_id: int,
    author_data: schemas.AuthorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_session),
):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    author.name = author_data.name
    author.email = author_data.email

    db.commit()
    db.refresh(author)

    return author


@app.delete("/authors/{author_id}", tags=["Authors"])
def delete_author(
    author_id: int, db: Session = Depends(get_db), current_user=Depends(require_session)
):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    db.delete(author)
    db.commit()

    return {"message": "Author deleted successfully"}


@app.post("/books", response_model=schemas.BookResponse, tags=["Books"])
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_session),
):
    author = db.query(models.Author).filter(models.Author.id == book.author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    new_book = models.Book(
        title=book.title,
        description=book.description,
        price=book.price,
        author_id=book.author_id,
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


@app.get("/books", response_model=list[schemas.BookResponse], tags=["Books"])
def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


@app.get("/books/{book_id}", response_model=schemas.BookResponse, tags=["Books"])
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.put("/books/{book_id}", response_model=schemas.BookResponse, tags=["Books"])
def update_book(
    book_id: int,
    book_data: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_session),
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    author = (
        db.query(models.Author).filter(models.Author.id == book_data.author_id).first()
    )

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    book.title = book_data.title
    book.description = book_data.description
    book.price = book_data.price
    book.author_id = book_data.author_id

    db.commit()
    db.refresh(book)

    return book


@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(
    book_id: int, db: Session = Depends(get_db), current_user=Depends(require_session)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()

    return {"message": "Book deleted successfully"}


@app.post("/logout", tags=["Authentication"])
def logout(request: Request):
    request.session.clear()

    return {"message": "Logout successful"}
