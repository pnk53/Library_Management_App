from libmgmt_app_backend import create_flask_app
from libmgmt_app_backend.extensions import db
from werkzeug.security import generate_password_hash

#Adding Librarian for admin role
def add_admin():
    from libmgmt_app_backend.models.user import User
    records = User.query.all()
    if not records:
        admin = User(userType="Librarian", visitedToday=False, flagged=False, firstName="admin", lastName="admin", email="admin@lms.com", username="admin123", password=generate_password_hash("admin123", method="scrypt", salt_length=16))
        db.session.add(admin)
        db.session.commit()
        print("Admin created")

#Main method
if __name__ == '__main__':
    app = create_flask_app()
    db.create_all()
    print("Tables created")
    add_admin()
    app.run(debug=True)