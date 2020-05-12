import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Photos(SqlAlchemyBase, UserMixin):
    __tablename__ = 'photos'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
