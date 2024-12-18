from pixegami_hellos.cam_db_config import db
from pixegami_hellos.organizations import Organizations
from pixegami_hellos.providers import Providers
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poc_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    
    db.create_all()
    new_org = Organizations(org_name="godhumala's room", csp_id=1)
    db.session.add(new_org)
    db.session.commit()

    
    organizations = Organizations.query.all()

    
    for org in organizations:
        print(org.org_name)
