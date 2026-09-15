from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthorCreate(BaseModel):
    name: str
    email: EmailStr


class AuthorResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {"from_attributes": True}


class BookCreate(BaseModel):
    title: str
    description: str | None = None
    price: float
    author_id: int


class BookResponse(BaseModel):
    id: int
    title: str
    description: str | None
    price: float
    author_id: int

    model_config = {"from_attributes": True}
