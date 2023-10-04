from random import randrange
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
 
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

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}") # id - path parameter
def get_posts(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exists")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exists")
    
    return {"message": updated_post}


