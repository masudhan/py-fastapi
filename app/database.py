from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from .config import settings

# postgresql://username:password@hostname:port/db-name
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
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
'''        