from datetime import datetime,timezone
from pixegami_hellos.cam_db_config import db

# Initilize the SQLAlchmy object


class Providers(db.Model):
    __tablename__ = 'csp_vendor'

    csp_id = db.Column(db.Integer, primary_key=True)
    csp_name = db.Column(db.String(3), unique=True)
    create_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Provider_vamshi {self.csp_name}>"
