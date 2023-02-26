from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


# Construção de uma postagem
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# responsavel pelo que ira retornar para o usuario
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# responsavel pelo que ira retornar para o usuario
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


#  criando uma classe para dizer o que o usuario precisa informar
class UserCreate(BaseModel):
    email: EmailStr  # isso garante que a informação seja um endereço eletrónico, e não apenas um texto aleatorio.
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# reponsavel pelo que esperamos que o login do usuario retorne
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
