from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey(Users.id))
    title = Column(String, unique=True)
    content = Column(String)
    # likes = Column(MutableList.as_mutable(PickleType), default=[])
    # dislikes = Column(MutableList.as_mutable(PickleType), default=[])


class PostReactions(Base):
    __tablename__ = "post_reactions"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey(Posts.id))
    user_id = Column(Integer, ForeignKey(Users.id))
    reaction = Column(String)
