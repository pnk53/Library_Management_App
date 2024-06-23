from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from sqlalchemy.orm import DeclarativeBase

api = Api(prefix="/api")

class BaseClass(DeclarativeBase):
    __abstratc__ = True

db = SQLAlchemy(model_class=BaseClass)