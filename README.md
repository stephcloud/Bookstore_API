# Bookstore API

A backend REST API for managing authors and books, built with FastAPI, PostgreSQL, SQLAlchemy, and Alembic. The application is containerized with Docker and Docker Compose.

## Features

- Create, read, update, and delete authors
- Create, read, update, and delete books
- Author-book relationship using a foreign key
- PostgreSQL database
- SQLAlchemy ORM
- Alembic database migrations
- Session-based authentication for write operations
- Docker and Docker Compose support
- Automatic database migration when the API container starts
- Interactive API documentation with Swagger UI

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL 18
- Alembic
- Pydantic
- Docker
- Docker Compose
- Uvicorn

## Project Structure

```text
bookstore/
├── alembic/
│   ├── versions/
│   │   └── add414fb3a6e_create_authors_and_books_tables.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── .dockerignore
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
Database Models
Author

The Author table contains:

id
name
email
Book

The Book table contains:

id
title
description
price
author_id

Each book is linked to an author through the author_id foreign key.

Authentication

The API uses session-based authentication for write operations.

Demo Login
Username: admin
Password: admin123

Login endpoint:

POST /login

After successful login, a session cookie is created.

Write operations require authentication.

Public operations include the GET endpoints.

API Endpoints
Authentication
Method	Endpoint	Description
POST	/login	Login
POST	/logout	Logout
Authors
Method	Endpoint	Description
POST	/authors	Create an author
GET	/authors	Get all authors
GET	/authors/{author_id}	Get one author
PUT	/authors/{author_id}	Update an author
DELETE	/authors/{author_id}	Delete an author
Books
Method	Endpoint	Description
POST	/books	Create a book
GET	/books	Get all books
GET	/books/{book_id}	Get one book
PUT	/books/{book_id}	Update a book
DELETE	/books/{book_id}	Delete a book
Database Migrations

Alembic is used to manage database schema changes.

The initial migration creates:

authors
books
The foreign key relationship between books and authors

Migration commands:

alembic upgrade head

Check the current migration:

alembic current

View migration history:

alembic history

The current migration is:

add414fb3a6e (head)
Running Locally
1. Create and activate the virtual environment
python -m venv venv
source venv/Scripts/activate
2. Install dependencies
pip install -r requirements.txt
3. Configure environment variables

Create a .env file:

DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/bookstore
SECRET_KEY=your-secret-key
4. Run migrations
alembic upgrade head
5. Start the application
uvicorn app.main:app --reload

Open Swagger UI:

http://127.0.0.1:8000/docs
Running with Docker

Build and start the application:

docker compose up --build

Docker Compose starts:

PostgreSQL
The FastAPI application

The API waits for PostgreSQL to become healthy before starting.

Alembic migrations are automatically applied when the API container starts.

Open Swagger UI:

http://localhost:8000/docs

To stop the containers:

docker compose down

To stop the containers and remove the database volume:

docker compose down -v

Docker Flow

## Architecture


flowchart TD
    Client[Client / Browser] --> Swagger[Swagger UI]
    Swagger --> FastAPI[FastAPI Application]

    FastAPI --> Auth[Session Authentication]
    FastAPI --> SQLAlchemy[SQLAlchemy ORM]

    SQLAlchemy --> PostgreSQL[(PostgreSQL Database)]
    Alembic[Alembic Migrations] --> PostgreSQL

    Docker[Docker Compose] --> FastAPI
    Docker --> PostgreSQL

Testing

The API was tested through Swagger UI.

The following were tested:

Author creation
Author retrieval
Author retrieval by ID
Author update
Author deletion
Book creation
Book retrieval
Book retrieval by ID
Book update
Book deletion
Login
Session authentication
Dockerized API
PostgreSQL connection
Alembic migrations

Alembic was also verified using:

alembic current
alembic history
Security Note

The authentication credentials used in this project are demonstration credentials for the assignment. A production application should use a database-backed user system with securely hashed passwords and properly managed secrets.