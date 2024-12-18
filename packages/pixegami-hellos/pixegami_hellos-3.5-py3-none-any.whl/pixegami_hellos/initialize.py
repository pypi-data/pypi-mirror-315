from flask import Flask
from pixegami_hellos.cam_db_config import db

def create_app(database_uri="sqlite:///poc_database.db"):
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

#    table creation 
    with app.app_context():
        db.create_all()

    return app
