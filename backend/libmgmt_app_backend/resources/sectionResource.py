from flask import abort
from flask_restful import Resource, marshal_with, reqparse, fields
from sqlalchemy.exc import IntegrityError
from libmgmt_app_backend.extensions import db, cache
from libmgmt_app_backend.main.routes import jwt_token_required
from libmgmt_app_backend.models.section import Section

section_parser = reqparse.RequestParser()
section_parser.add_argument("name", type=str, required=True)
section_parser.add_argument("dateCreated", type=str, required=True)
section_parser.add_argument("description", type=str)
section_parser.add_argument("rating", type=int)

section_update_parser = reqparse.RequestParser()
section_update_parser.add_argument("name", type=str)
section_update_parser.add_argument("dateCreated", type=str)
section_update_parser.add_argument("description", type=str)
section_update_parser.add_argument("rating", type=int)

section_fields={
    "id": fields.Integer,
    "name": fields.String,
    "dateCreated": fields.String,
    "description": fields.String,
    "rating": fields.Integer,
}

def section_not_found(section_id):
    currentSection = Section.query.get(section_id)
    if not currentSection:
        abort(
            404,
                {
                    "message": "Section {} doesn't exist".format(section_id),
                    "data": section_id,
                    "error": "404 Not Found",
                }
        )

class SectionResource(Resource):
    @jwt_token_required
    @cache.cached(timeout=50)
    @marshal_with(section_fields)
    def get(self,section_id=None):
        if section_id:
            section_not_found(section_id)
            currentSection = Section.query.get(section_id)
            print("Fetching section from database")
            return currentSection, 200
        else:
            allSections = Section.query.all()
            print("Fetching all sections from database")
            return allSections, 200
    
    @jwt_token_required
    @marshal_with(section_fields)
    def put(self, section_id=None):
        if section_id:
            section_not_found(section_id)
            data = section_update_parser.parse_args()
            currentSection = Section.query.get(section_id)
            for d in data:
                if data[d] is not None:
                    setattr(currentSection, d, data[d])
            db.session.commit()
            cache.clear()
            return currentSection, 200
    
    @jwt_token_required
    @marshal_with(section_fields)
    def post(self):
        data = section_parser.parse_args()
        newSection = Section(**data)
        try:
            db.session.add(newSection)
            db.session.commit()
            cache.clear()
        except IntegrityError as e:
            db.session.rollback()
            abort(409,{
                "message": "Section {} already exist".format(newSection.name),
                "data": None,
                "error": str(e),
            })
        return newSection, 201
    
    @jwt_token_required
    @marshal_with(section_fields)
    def delete(self, section_id):
        if section_id:
            section_not_found(section_id)
            currentSection = Section.query.get(section_id)
            try:
                db.session.delete(currentSection)
                db.session.commit()
                cache.clear()
            except Exception as e:
                abort(500,{
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e),
                })
            return currentSection, 200