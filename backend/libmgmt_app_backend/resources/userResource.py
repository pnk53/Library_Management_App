from flask import abort
from flask_restful import Resource, marshal_with, reqparse, fields
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from libmgmt_app_backend.extensions import db
from libmgmt_app_backend.main.routes import jwt_token_required
from libmgmt_app_backend.models.user import User

user_parser = reqparse.RequestParser()
user_parser.add_argument("userType", type=str, required=True)
user_parser.add_argument("visitedToday", type=bool, required=True)
user_parser.add_argument("flagged", type=bool, required=True)
user_parser.add_argument("firstName", type=str, required=True)
user_parser.add_argument("lastName", type=str)
user_parser.add_argument("email", type=str, required=True)
user_parser.add_argument("username", type=str, required=True)
user_parser.add_argument("password", type=str, required=True)

user_update_parser = reqparse.RequestParser()
user_update_parser.add_argument("userType", type=str)
user_update_parser.add_argument("visitedToday", type=bool)
user_update_parser.add_argument("flagged", type=bool)
user_update_parser.add_argument("firstName", type=str)
user_update_parser.add_argument("lastName", type=str)
user_update_parser.add_argument("email", type=str)
user_update_parser.add_argument("username", type=str)
user_update_parser.add_argument("password", type=str)

user_fields={
    "id": fields.Integer,
    "userType": fields.String,
    "visitedToday": fields.Boolean,
    "flagged": fields.Boolean,
    "firstName": fields.String,
    "lastName": fields.String,
    "email": fields.String,
    "username": fields.String,
}

def user_not_found(user_id):
    currentUser = User.query.get(user_id)
    if not currentUser:
        abort(
            404,
                {
                    "message": "User {} doesn't exist".format(user_id),
                    "data": user_id,
                    "error": "404 Not Found",
                }
        )

class UserResource(Resource):
    @jwt_token_required
    @marshal_with(user_fields)
    def get(self,user_id=None):
        if user_id:
            user_not_found(user_id)
            currentUser = User.query.get(user_id)
            print("Fetching user from database")
            return currentUser, 200
        else:
            allUsers = User.query.all()
            print("Fetching all users from database")
            return allUsers, 200
    
    @jwt_token_required
    @marshal_with(user_fields)
    def put(self, user_id=None):
        if user_id:
            user_not_found(user_id)
            data = user_update_parser.parse_args()
            currentUser = User.query.get(user_id)
            for d in data:
                if data[d] is not None:
                    setattr(currentUser, d, data[d])
            db.session.commit()
            return currentUser, 200
            
    @marshal_with(user_fields)
    def post(self):
        data = user_parser.parse_args()
        newUser = User(userType="User", visitedToday=False, flagged=False, firstName=data.firstName, lastName=data.lastName, email=data.email, username=data.username, password=generate_password_hash(data.password, method="scrypt", salt_length=16))
        try:
            db.session.add(newUser)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(409,{
                "message": "User {} already exist".format(newUser.username),
                "data": None,
                "error": str(e),
            })
        return newUser, 201
        
    @jwt_token_required
    @marshal_with(user_fields)
    def delete(self, user_id):
        if user_id:
            user_not_found(user_id)
            currentUser = User.query.get(user_id)
            try:
                db.session.delete(currentUser)
                db.session.commit()
            except Exception as e:
                abort(500,{
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e),
                })
            return currentUser, 200