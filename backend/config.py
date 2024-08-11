import os
class LocalConfig:
    JWT_SECRET_KEY = "thisismysecretjwtkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///LIBmgmtDB.sqlite3"
    UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + "\libmgmt_app_backend"
    PARENT_PATH = "http://localhost:5000/static/"