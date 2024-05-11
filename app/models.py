from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable= False,unique=True)
    password = Column(String,nullable=False,unique= True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='True',nullable=False)
    rating = Column(Integer,server_default='0',nullable=False)
    owner_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))

    owner = relationship('User')


class Votes(Base):
    __tablename__ = "votes"

    post_id = Column(Integer,ForeignKey('posts.id',ondelete='CASCADE'),primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),primary_key=True)