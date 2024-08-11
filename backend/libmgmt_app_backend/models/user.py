from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from werkzeug.security import check_password_hash
from libmgmt_app_backend.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True, primary_key=True)
    userType = Column(String(50), nullable=False)
    visitedToday = Column(Boolean, default=False, nullable=False)
    flagged = Column(Boolean, default=False, nullable=False)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100))
    email = Column(String(200), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(1000), nullable=False)
    book = db.relationship('Book', backref='user', lazy=True)
    issuedBook = db.relationship('IssuedBook', backref='user', lazy=True)
    
    def __init__(self, userType, visitedToday, flagged, firstName, lastName, email, username, password):
        self.userType = userType
        self.visitedToday = visitedToday
        self.flagged = flagged
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.username = username
        self.password = password
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_librarian(self):
        return self.userType == "Librarian"
    
    def __repr__(self):
        return "<User {}>".format(self.username)