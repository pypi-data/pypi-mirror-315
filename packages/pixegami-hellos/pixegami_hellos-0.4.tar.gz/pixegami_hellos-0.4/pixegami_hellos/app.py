from flask import Flask
from cam_db_config import db
from models.providers import Providers
from models.organizations import Organizations

app = Flask(__name__)

# SQLite database URI (for PoC)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poc_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db object with Flask
db.init_app(app)

@app.route('/')
def home():
    return "Welcome to the Flask App!"

# Create the database tables
with app.app_context():
    db.create_all()  # This will create the tables defined in your models

if __name__ == '__main__':
    app.run(debug=True)
