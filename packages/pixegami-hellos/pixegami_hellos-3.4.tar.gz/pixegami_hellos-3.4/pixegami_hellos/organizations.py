from datetime import datetime, timezone
from pixegami_hellos.cam_db_config import db
from pixegami_hellos.providers import Providers

class Organizations(db.Model):
    __tablename__ = 'cisco_org_master'

    org_id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(45))
    csp_id = db.Column(db.Integer, db.ForeignKey(Providers.csp_id), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Define the relationship with Providers
    provider = db.relationship('Providers', backref='organizations')

    def __repr__(self):
        return f"<Organization {self.org_name}>"
