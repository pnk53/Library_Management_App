from flask_login import UserMixin
from sqlalchemy import Column, Integer, Sequence, String

from libmgmt_app_backend.extensions import db

class Section(db.Model, UserMixin):
    __tablename__ = "section"
    id = Column(Integer, Sequence('section_id_seq', start=101, increment=1), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    dateCreated = Column(String(50), nullable=False)
    description = Column(String(500))
    rating = Column(Integer)
    
    def __init__(self, name, dateCreated, description, rating):
        self.name = name
        self.dateCreated = dateCreated
        self.description = description
        self.rating = rating
    
    def __repr__(self):
        return "<User {}>".format(self.name)