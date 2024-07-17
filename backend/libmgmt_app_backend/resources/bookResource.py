from flask import abort
from flask_restful import Resource, marshal_with, reqparse, fields
from sqlalchemy.exc import IntegrityError
from libmgmt_app_backend.extensions import db
from libmgmt_app_backend.main.routes import jwt_token_required
from libmgmt_app_backend.models.book import Book

book_parser = reqparse.RequestParser()
book_parser.add_argument("status", type=str, required=True)
book_parser.add_argument("flagged", type=bool, required=True)
book_parser.add_argument("title", type=str, required=True)
book_parser.add_argument("author", type=str, required=True)
book_parser.add_argument("language", type=str, required=True)
book_parser.add_argument("releaseDate", type=str, required=True)
book_parser.add_argument("section", type=str, required=True)
book_parser.add_argument("contentPath", type=str, required=True)
book_parser.add_argument("currentIssuer", type=int)
book_parser.add_argument("issuedDate", type=str)
book_parser.add_argument("returnedDate", type=str)
book_parser.add_argument("rating", type=int, required=True)
book_parser.add_argument("totalRater", type=int, required=True)

book_fields={
    "id": fields.Integer,
    "status": fields.String,
    "flagged": fields.Boolean,
    "title": fields.String,
    "author": fields.String,
    "language": fields.String,
    "releaseDate": fields.String,
    "section": fields.String,
    "contentPath": fields.String,
    "currentIssuer": fields.Integer,
    "issuedDate": fields.String,
    "returnedDate": fields.String,
    "rating": fields.Integer,
    "totalRater": fields.Integer,
}

def book_not_found(book_id):
    currentBook = Book.query.get(book_id)
    if not currentBook:
        abort(
            404,
                {
                    "message": "Book {} doesn't exist".format(book_id),
                    "data": book_id,
                    "error": "404 Not Found",
                }
        )

class BookResource(Resource):
    @jwt_token_required
    @marshal_with(book_fields)
    def get(self,book_id=None):
        if book_id:
            book_not_found(book_id)
            currentBook = Book.query.get(book_id)
            print("Fetching book from database")
            return currentBook, 200
        else:
            allBooks = Book.query.all()
            print("Fetching all books from database")
            return allBooks, 200
    
    @jwt_token_required
    @marshal_with(book_fields)
    def put(self, book_id=None):
        if book_id:
            book_not_found(book_id)
            data = book_parser.parse_args()
            currentBook = Book.query.get(book_id)
            for d in data:
                if data[d] is not None:
                    setattr(currentBook, d, data[d])
            db.session.commit()
            return currentBook, 200
    
    @jwt_token_required
    @marshal_with(book_fields)
    def post(self):
        data = book_parser.parse_args()
        newBook = Book(**data)
        try:
            db.session.add(newBook)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(409,{
                "message": "Book {} already exist".format(newBook.title),
                "data": None,
                "error": str(e),
            })
        return newBook, 201
    
    @jwt_token_required
    @marshal_with(book_fields)
    def delete(self, book_id):
        if book_id:
            book_not_found(book_id)
            currentBook = Book.query.get(book_id)
            try:
                db.session.delete(currentBook)
                db.session.commit()
            except Exception as e:
                abort(500,{
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e),
                })
            return currentBook, 200