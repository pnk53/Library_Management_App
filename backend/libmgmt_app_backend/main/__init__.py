from flask import Blueprint

bpMain = Blueprint('main',__name__)

from libmgmt_app_backend.main import routes