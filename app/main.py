from fastapi import FastAPI
from .database import engine
from . import models
from .config import settings
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware 
from alembic import command

# this will tell sqlalchemy to run the create statements
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# command.upgrade("head")

origins = ['*']

app.add_middleware(
    CORSMiddleware, #middle is a function that runs before for every request 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Path operation
@app.get("/")  # Decorator
def root():
    return {"message": "Hello Madhu, deployed through CI/CD!!!"}
