from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean

from libmgmt_app_backend.extensions import db

class Book(db.Model, UserMixin):
    __tablename__ = "book"
    id = Column(Integer, autoincrement=True, primary_key=True)
    status = Column(String(50), nullable=False)
    flagged = Column(Boolean, default=False, nullable=False)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    language = Column(String(100), nullable=False)
    releaseDate = Column(String(50), nullable=False)
    section = Column(String(200), nullable=False)
    contentPath = Column(String(200), nullable=False)
    issuedDate = Column(String(50))
    returnedDate = Column(String(50))
    rating = Column(Integer, nullable=False)
    totalRater = Column(Integer, nullable=False)
    currentIssuer = Column(Integer, db.ForeignKey('user.id'))
    issuedBook = db.relationship('IssuedBook', backref='book', lazy=True)
    
    def __init__(self, status, flagged, title, author, language, releaseDate, section, contentPath, currentIssuer, issuedDate, returnedDate, rating, totalRater):
        self.status = status
        self.flagged = flagged
        self.title = title
        self.author = author
        self.language = language
        self.releaseDate = releaseDate
        self.section = section
        self.contentPath = contentPath
        self.currentIssuer = currentIssuer
        self.issuedDate = issuedDate
        self.returnedDate = returnedDate
        self.rating = rating
        self.totalRater = totalRater
    
    def __repr__(self):
        return "<Book {}>".format(self.id)