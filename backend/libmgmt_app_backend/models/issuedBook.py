from flask_login import UserMixin
from sqlalchemy import Column, Integer, String

from libmgmt_app_backend.extensions import db

class IssuedBook(db.Model, UserMixin):
    __tablename__ = "issuedBook"
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(50), nullable=False)
    issuedDate = Column(String(50), nullable=False)
    returnedDate = Column(String(50), nullable=False)
    bookId = Column(Integer, db.ForeignKey('book.id'), nullable=False)
    userId = Column(Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, status, bookId, userId, issuedDate, returnedDate):
        self.status = status
        self.bookId = bookId
        self.userId = userId
        self.issuedDate = issuedDate
        self.returnedDate = returnedDate
    
    def __repr__(self):
        return "<IssuedBook {}>".format(self.id)