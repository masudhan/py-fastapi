from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm  import Session
from . import models
from .database import engine, get_db
 
models.Base.metadata.create_all(bind=engine) 

app = FastAPI()


# Define class, extend BaseModel - pydantic - This is for schema and validation
class Post(BaseModel):
    title:  str
    content: str
    published: bool = False

while True:

    try:
        conn = psycopg2.connect(host = '172.17.0.3', database = "ms-fastapi", user = "postgres", password = 'madhu@123', cursor_factory=RealDictCursor)

        cursor = conn.cursor()

        print("Database connection was successful!")
        break
    except Exception as error:
        print("Database connection Failed")
        print("Error: ", error)
        time.sleep(2)


my_posts = [{'title': 'title of 1st post', 'content': 'content of 1st post', 'published': True, 'rating': 4 , "id": 1},{'title': 'title of 2nd post', 'content': 'content of 2nd post', 'published': True, 'rating': 5, "id": 2 }]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index


# Path operation
@app.get("/") #Decorator
def root():
    return {"message": "Hello Madhu"}

@app.get("/testing")
def testing(db: Session = Depends(get_db)):

    posts =  db.query(models.Post).all()

    return {"data": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts =  db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get("/posts/{id}") # id - path parameter
def get_posts(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exists")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exists")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()
    
    return {"message": post_query.first()}


