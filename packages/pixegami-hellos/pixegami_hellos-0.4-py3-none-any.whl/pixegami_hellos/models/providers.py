from datetime import datetime
from cam_db_config import db

class Providers(db.Model):
    __tablename__ = 'csp_vendor'

    csp_id = db.Column(db.Integer, primary_key=True)
    csp_name = db.Column(db.String(3), unique=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Provider {self.csp_name}>"
