# app.py
from flask import Flask, jsonify
from pixegami_hellos.cam_db_config import db
from pixegami_hellos.providers import Providers  # Import the Providers model
from pixegami_hellos.organizations import Organizations  # Import the Organizations model

app = Flask(__name__)

# SQLite database URI (for PoC)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poc_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db object with Flask
db.init_app(app)

@app.route('/')
def create_organization():
    
    new_org = Organizations(org_name="New Organizationvjhhjhjgj", csp_id=1)
    db.session.add(new_org)
    db.session.commit()
    return f"Organization {new_org.org_name} added."

@app.route('/create_provider')
def create_provider():
   
    new_provider = Providers(csp_name="AWS")
    db.session.add(new_provider)
    db.session.commit()
    return f"Provider {new_provider.csp_name} added."
@app.route('/providers')
def get_providers():
    providers = Providers.query.all()  
    providers_list = [provider.csp_name for provider in providers]
    return jsonify(providers=providers_list)

@app.route('/organizations')
def get_organizations():
    organizations = Organizations.query.all()  
    org_list = [org.org_name for org in organizations]
    return jsonify(organizations=org_list)

@app.route('/')
def home():
    return "Welcome to the Flask App!"


with app.app_context():
    db.create_all()  
    

if __name__ == '__main__':
    app.run(debug=True,port=5016)
