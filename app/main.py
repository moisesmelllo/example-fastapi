from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import posts, users, auth, vote
from .config import settings

print(settings.database_username)

# models.Base.metadata.create_all(bind=engine)  # cria a mesa e as colunas no banco de dados, caso não tenha
# não é mais necessarios pois utilizamos alembic

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


# The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.
@app.get('/')
def root():
    return {'message': 'boraaa!!!!'}
