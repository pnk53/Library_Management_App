from datetime import datetime, timedelta
from functools import wraps
from flask import jsonify, make_response, request
from jwt import decode, encode
from config import LocalConfig
from libmgmt_app_backend.models.user import User
from libmgmt_app_backend.main import bpMain

def jwt_token_required(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        token=None
        
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            
        response = {"message": {"error": ""}}
        
        if not token:
            response["message"]["error"] = "JWT token missing"
            return make_response(response, 401)
        
        jwt_data=None
        try:
            jwt_data = decode(
                token,
                LocalConfig.JWT_SECRET_KEY,
                algorithms=["HS256"],
            )
            
            currentUser = User.query.filter_by(username=jwt_data["name"]).first()
            if not currentUser:
                response["message"]["error"]=f"User {jwt_data['name']} doesn't exist"
                return make_response(response, 404)
            
            token_exp = datetime.utcfromtimestamp(jwt_data["exp"])
            current_time = datetime.utcnow()
            if token_exp < current_time:
                response["message"]["error"] = "JWT token has expired"
                return make_response(response, 401)
            
        except Exception as e:
            return{
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500
            
        return f(*args, **kwargs)
    
    return decorator

@bpMain.route("/login", methods=["POST"])
def userLogin():
    try:
        username = request.json.get("username","")
        password = request.json.get("password","")
    
        currentUser = User.query.filter_by(username=username).first()
    
        if not currentUser:
            return jsonify(
                {
                    "message": "User {} doesn't exist.".format(username),
                    "data": username,
                    "error": "404 Not Found"
                }
            ), 404
        
        if not currentUser.check_password(password):
            return jsonify(
                {
                    "message": "Wrong credentials. Please check your username and password.",
                    "data": username,
                    "error": "User {} unauthorized.".format(username)
                }
            ), 401
        
        jwt = encode(
            {
                "name": username,
                "user_id": currentUser.id,
                "exp": datetime.utcnow() + timedelta(minutes=2)
            },
            LocalConfig.JWT_SECRET_KEY,
            algorithm="HS256",
        )
        
        return jsonify(
            {
                "status": "ok",
                "jwt": jwt,
                "name": username,
                "user_id": currentUser.id,
                "exp": (datetime.utcnow() + timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S'),
            }
        ), 201
        
    except Exception as e:
        return jsonify(
            {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }
        ), 500