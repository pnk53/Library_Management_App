from flask import Flask
from flask_cors import CORS
from config import LocalConfig

def create_flask_app(configuration=LocalConfig):
    flask_app = Flask(__name__)
    flask_app.config.from_object(configuration)
    flask_app.app_context().push()
    
    #Initialize Flask extensions here
    from libmgmt_app_backend.extensions import db, api
    db.__init__(flask_app)
    
    CORS(
        flask_app,
        origins="http://localhost:8081",
    )
    
    #Register blueprints here
    
    
    api.init_app(flask_app)
    
    @flask_app.route('/test/')
    def testPage():
        return '<h1>This is the testing page for "/test/" url</h1> <h2>This is successful !!!!</h2>'
    
    @flask_app.route('/api/healthcheck')
    def healthcheck():
        return {"status" : "ok"}
    
    return flask_app