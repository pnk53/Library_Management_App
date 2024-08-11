from flask_login import UserMixin
from sqlalchemy import Column, Integer, String

from libmgmt_app_backend.extensions import db

class IssuedBook(db.Model, UserMixin):
    __tablename__ = "issuedBook"
    id = Column(Integer, autoincrement=True, primary_key=True)
    status = Column(String(50), nullable=False)
    issuedDate = Column(String(50))
    returnedDate = Column(String(50))
    bookName = Column(String(100), nullable=False)
    issuerName = Column(String(50), nullable=False)
    bookId = Column(Integer, db.ForeignKey('book.id'), nullable=False)
    userId = Column(Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, status, bookId, userId, issuedDate, returnedDate, bookName, issuerName):
        self.status = status
        self.bookId = bookId
        self.userId = userId
        self.issuedDate = issuedDate
        self.returnedDate = returnedDate
        self.bookName = bookName
        self.issuerName = issuerName
    
    def __repr__(self):
        return "<IssuedBook {}>".format(self.id)