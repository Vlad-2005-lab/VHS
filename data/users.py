import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    friends = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    request = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_data = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    videos = sqlalchemy.Column(sqlalchemy.String, nullable=True)
