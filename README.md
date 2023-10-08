## Tech Stack

Python </br>
FastAPI framework</br>
Postgres</br>
SQL Alchemy</br>
Alembic </br>

Social media type application where users can create posts, they can read other people's posts, they'll be able to perform all the CRUD operations. And we'll also be able to vote(or like) on posts. 

## Env setup

python3
vscode
virtual environment (python3 -m venv venv; source venv/bin/activate)

## packages

pip install 'fastapi[all]'
pip freeze

## Run the program
uvicorn main:app --reload

## Why Schema
It's a pain to get all the values from the body </br>
The client can send whatever they want </br>
The data isn't getting validated </br>
We ultimately want to force the client to send data in a schema that we expect </br>

## CRUD

Create  -  POST  - /posts       -       @app.post("/posts")

Read    -  GET   - /posts/:id   -       @app.get("/posts/{id}") </br>
        -  GET   - /posts       -       @app.get("/posts/")

Update  -  PUT/PATCH   - /posts/:id   -       @app.put("/posts/{id}")

Delete  -  DELETE   - /posts/:id   -       @app.delete("/posts/{id}")

## Swagger

Built-in feature os fastAPI

http://127.0.0.1:8000/docs

Documentation tool - http://127.0.0.1:8000/redoc

## Restructure

Before this main.py file is outside the app folder, we created and __init__.py in app folder to act as a package

Now to run the program - `uvicorn app.main:app --reload`


## Setting up the database



| Data Type | Postgres | Python |
| --- | --- | --- |
| Numeric   | int, decimal, precision   | int, float |
| Text   | varchar, text   | string |
| Boolean   |  boolean  | boolean |
| Sequence   |  array  | list  |


### Constraints

When we create a table we have to specify `primary key`, it is a column or group of columns that uniquely identifies each row in a table

Table can have one and only one primary key

Each entry must be unique, no duplicates

Primary key doesn't have to be the ID column always. It's up to you to decide which column uniquely defines each record

email column can also be used as the primary key

What happens if we have another column that isn't the primary key, but we want to ensure that each and every entry has a unique value for that column

A `UNIQUE` constraint can be applied to any column to make sure every record has a unique value for that column

ex: `username` when signing up 

By default, when adding a new entry to a db, any column can be left blank. When a column is left blank, it has a null value

If you need column to be properly filled in to create a new record, a `NOT NULL` constraint can be added to the column to ensure that the column is never left blank

ex: `NOT NULL` constraint on age column 

```
CREATE DATABASE IF NOT EXISTS ms-fastapi
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

CREATE TABLE IF NOT EXISTS public.products
(
    name character varying NOT NULL,
    price integer NOT NULL,
    id serial,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.products
    OWNER to postgres;

INSERT INTO products (name, price, inventory) VALUES ('CAR', 25000, 30), ('LAPTOP', 90000, 10) returning *;

DELETE FROM products WHERE id = 10 RETURNING *;

UPDATE products SET is_sale = true WHERE inventory = 0 RETURNING *;

```    

`sudo apt-get install libpq-dev `

`pg_config is in postgresql-devel (libpq-dev in Debian/Ubuntu, libpq-devel on Centos/Fedora/Cygwin/Babun.)`

`pip install psycopg2`

`sudo apt-get install python3-tk`


### Object Relational Mapper(ORM)

There are couple of different ways when interacting with the database. One is direct running SQL commands in the code and other way is using what's referred to as object relational mapper or an ORM. It's a layer of abstraction that sits between the database and our fastapi application so we never actually talk directly with db anyone, we talk to the ORM and then it'll talk to our DB. Some of the benefits are we don't actually work with SQL anymore. So instead of using raw SQL, we'll actually use standard python code calling various functions and methods that alternately translate into SQL themselves. 

So instead of manually defining tables in postgres, we can define our tables as python models

SQLalchemy is one of the most popular python ORMs

`pip install sqlalchemy==1.4.23`


For storing password in db, we need to hash it, so in [fastapi documentation](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#:~:text=PassLib%20is%20a%20great%20Python%20package%20to%20handle%20password%20hashes.) we can use `passlib` package to handle passwords

`pip install "passlib[bcrypt]"`

### Authentication

When working with authentication on an API, or any application, there's really two main ways to tackle authentication

1. Session based authentication - idea is a session is that we store something on our backend server or API in this case, to track whether a user is logged in. So there is some piece of information, whether we store in the db or memory that's going to keep track of if the user is logged in and when user logs out

2. Using JWT token based authentication. It's stateless, meaning there's nothing on our backend, there's nothing on our API, there's nothing in out db that actually keps track or stores some sort of information about whether a user is logged in or logged out. It's actually stored on the frontend of our clients, actually keeps track of whether a user is logged in or not


For JWT, `pip install "python-jose[cryptography]"`

To get secret_key `openssl rand -hex 32`

To add new columns to db, right now it's not possible with sqlalchemy. We can use Alembic, Alembic provides for the creation, management, and invocation of change management scripts for a relational database, using SQLAlchemy as the underlying engine.

`pip install alembic`

`alembic init alembic`

`alembic revision -m "create posts table"`

`alembic current`

`alembic upgrade 23841ecc28ec`

To upgrade/create tables automatically based on the models we have - `alembic revision --autogenerate -m "auto-vote"`


