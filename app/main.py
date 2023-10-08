from fastapi import FastAPI
from .database import engine
from . import models
from .config import settings
from .routers import post, user, auth, vote

# this will tell sqlalchemy to run the create statements
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Path operation
@app.get("/")  # Decorator
def root():
    return {"message": "Hello Madhu"}
