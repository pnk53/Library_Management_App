from datetime import datetime
import os
from flask import Flask, jsonify, send_file, send_from_directory
from flask_cors import CORS
from config import LocalConfig

flask_app = None

def create_flask_app(configuration=LocalConfig):
    global flask_app
    flask_app = Flask(__name__)
    flask_app.config.from_object(configuration)
    flask_app.app_context().push()
    
    #Initialize Flask extensions here
    from libmgmt_app_backend.extensions import db, api, cache, celery_app
    db.__init__(flask_app)
    
    CORS(
        flask_app,
        origins="http://localhost:8081",
    )
    cache.init_app(
        flask_app,
        config={
            "CACHE_TYPE": "redis",
            "CACHE_REDIS_URL": "redis://localhost:6379/1",
            "prefix": "cache_",
        },
    )
    
    celery_app.conf.update(flask_app.config)
    
    #Register blueprints here
    from libmgmt_app_backend.main import bpMain
    flask_app.register_blueprint(bpMain)
    
    #Add your resources here
    from libmgmt_app_backend.resources.userResource import UserResource
    from libmgmt_app_backend.resources.bookResource import BookResource
    from libmgmt_app_backend.resources.sectionResource import SectionResource
    from libmgmt_app_backend.resources.issuedBookResource import IssuedBookResource
    
    api.add_resource(UserResource, "/user", "/user/<int:user_id>")
    api.add_resource(BookResource, "/book", "/book/<int:book_id>")
    api.add_resource(SectionResource, "/section", "/section/<int:section_id>")
    api.add_resource(IssuedBookResource, "/issuedBook", "/issuedBook/<int:issuedBook_id>")
    
    api.init_app(flask_app)
    
    @flask_app.route('/test/')
    def testPage():
        return '<h1>This is the testing page for "/test/" url</h1> <h2>This is successful !!!!</h2>'
    
    @flask_app.route('/api/healthcheck')
    @cache.cached(timeout=10)
    def healthcheck():
        return jsonify({"status" : "ok",
                "datetime" : datetime.now()})
    
    @flask_app.route('/celeryDemo')
    def celeryDemo():
        from tasks import add
        result = add.delay(10,20)
        return jsonify({"task_id": result.id})
    
    @flask_app.route('/download-csv')
    def downloadCSV():
        from tasks import export_csv_task
        result = export_csv_task.delay()
        return jsonify({"task_id": result.id, "message": "CSV exported successfully"})
        
    return flask_app