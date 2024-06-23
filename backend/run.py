from libmgmt_app_backend import create_flask_app
from libmgmt_app_backend.extensions import db

#Main method
if __name__ == '__main__':
    app = create_flask_app()
    db.create_all()
    app.run(debug=True)