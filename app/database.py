from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# URL FORMAT = "postgresql://<username>:<password>@<ip-address or hostname>/<database-name>"

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL) # it manages connections with database
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine) # is is used to make session with engine in database

Base = declarative_base() 

'''
declarative_base() : 

Declarative Base: The term "declarative" refers to the ability to define the structure of your database tables and their relationships using Python classes and attributes, rather than writing SQL statements directly. SQLAlchemy's declarative base provides a way to define these mappings between your Python classes and database tables in a concise and readable manner.

Class Inheritance: When you call declarative_base(), it returns a base class from which all your SQLAlchemy model classes will inherit. This inheritance provides your model classes with various capabilities and features for interacting with the database.

Metadata Handling: The declarative_base() function also creates a MetaData object internally. This MetaData object is a catalog that holds various aspects of your database schema, such as tables, columns, constraints, and relationships. By inheriting from the base class returned by declarative_base(), your model classes automatically have access to this metadata.

Table Creation: When you define your model classes by subclassing the base class returned by declarative_base(), SQLAlchemy inspects these classes and their attributes to automatically generate the corresponding database tables. This process is known as table reflection.
'''




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()