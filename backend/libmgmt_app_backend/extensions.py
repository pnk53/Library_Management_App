from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from sqlalchemy.orm import DeclarativeBase
from flask_caching import Cache

api = Api(prefix="/api")

cache = Cache()

class BaseClass(DeclarativeBase):
    __abstratc__ = True

db = SQLAlchemy(model_class=BaseClass)