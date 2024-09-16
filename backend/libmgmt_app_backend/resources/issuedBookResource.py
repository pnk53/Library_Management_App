from flask import abort
from flask_restful import Resource, marshal_with, reqparse, fields
from sqlalchemy.exc import IntegrityError
from libmgmt_app_backend.extensions import db, cache
from libmgmt_app_backend.main.routes import jwt_token_required
from libmgmt_app_backend.models.issuedBook import IssuedBook

issuedBook_parser = reqparse.RequestParser()
issuedBook_parser.add_argument("status", type=str, required=True)
issuedBook_parser.add_argument("bookName", type=str, required=True)
issuedBook_parser.add_argument("issuerName", type=str, required=True)
issuedBook_parser.add_argument("bookId", type=int, required=True)
issuedBook_parser.add_argument("userId", type=int, required=True)
issuedBook_parser.add_argument("issuedDate", type=str)
issuedBook_parser.add_argument("returnedDate", type=str)

issuedBook_update_parser = reqparse.RequestParser()
issuedBook_update_parser.add_argument("status", type=str)
issuedBook_parser.add_argument("bookName", type=str)
issuedBook_parser.add_argument("issuerName", type=str)
issuedBook_update_parser.add_argument("bookId", type=int)
issuedBook_update_parser.add_argument("userId", type=int)
issuedBook_update_parser.add_argument("issuedDate", type=str)
issuedBook_update_parser.add_argument("returnedDate", type=str)

issuedBook_fields={
    "id": fields.Integer,
    "status": fields.String,
    "bookName": fields.String,
    "issuerName": fields.String,
    "bookId": fields.Integer,
    "userId": fields.Integer,
    "issuedDate": fields.String,
    "returnedDate": fields.String,
}

def issuedBook_not_found(issuedBook_id):
    currentIssuedBook = IssuedBook.query.get(issuedBook_id)
    if not currentIssuedBook:
        abort(
            404,
                {
                    "message": "Issued Book {} doesn't exist".format(issuedBook_id),
                    "data": issuedBook_id,
                    "error": "404 Not Found",
                }
        )

class IssuedBookResource(Resource):
    @jwt_token_required
    @cache.cached(timeout=50)
    @marshal_with(issuedBook_fields)
    def get(self,issuedBook_id=None):
        if issuedBook_id:
            issuedBook_not_found(issuedBook_id)
            currentIssuedBook = IssuedBook.query.get(issuedBook_id)
            print("Fetching issuedBook from database")
            return currentIssuedBook, 200
        else:
            allIssuedBooks = IssuedBook.query.all()
            print("Fetching all issuedBooks from database")
            return allIssuedBooks, 200
    
    @jwt_token_required
    @marshal_with(issuedBook_fields)
    def put(self, issuedBook_id=None):
        if issuedBook_id:
            issuedBook_not_found(issuedBook_id)
            data = issuedBook_update_parser.parse_args()
            currentIssuedBook = IssuedBook.query.get(issuedBook_id)
            for d in data:
                if data[d] is not None:
                    setattr(currentIssuedBook, d, data[d])
            db.session.commit()
            cache.clear()
            return currentIssuedBook, 200
    
    @jwt_token_required
    @marshal_with(issuedBook_fields)
    def post(self):
        data = issuedBook_parser.parse_args()
        newIssuedBook = IssuedBook(**data)
        try:
            db.session.add(newIssuedBook)
            db.session.commit()
            cache.clear()
        except IntegrityError as e:
            db.session.rollback()
            abort(409,{
                "message": "Issued Book {} already exist".format(newIssuedBook.bookId),
                "data": None,
                "error": str(e),
            })
        return newIssuedBook, 201
    
    @jwt_token_required
    @marshal_with(issuedBook_fields)
    def delete(self, issuedBook_id):
        if issuedBook_id:
            issuedBook_not_found(issuedBook_id)
            currentIssuedBook = IssuedBook.query.get(issuedBook_id)
            try:
                db.session.delete(currentIssuedBook)
                db.session.commit()
                cache.clear()
            except Exception as e:
                abort(500,{
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e),
                })
            return currentIssuedBook, 200