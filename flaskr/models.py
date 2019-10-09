from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from flaskr.database import Base
from datetime import datetime


class User(Base):
    """ 用户模型类 """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(120), unique=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.username}>'


class Post(Base):
    """ 博客类 """
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now())
    title = Column(String(64), nullable=False)
    body = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, title, body, author_id):
        self.title = title
        self.body = body
        self.author_id = author_id

    def __repr__(self):
        return f'<Post {self.title}>'
        