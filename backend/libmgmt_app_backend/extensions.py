from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from sqlalchemy.orm import DeclarativeBase
from flask_caching import Cache

api = Api(prefix="/api")

cache = Cache()

celery_app = Celery(
    "tasks",
    broker="redis://127.0.0.1:6379/0",
    # backend="sqlite:///instance/celery.sqlite3",
    backend="redis://127.0.0.1:6379/0",
)

class BaseClass(DeclarativeBase):
    __abstratc__ = True

db = SQLAlchemy(model_class=BaseClass)