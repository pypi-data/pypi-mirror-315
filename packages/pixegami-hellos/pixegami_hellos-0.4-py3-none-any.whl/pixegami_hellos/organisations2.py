# import datetime

# from cam_db_config import db
# from .providers import Providers  # Import Providers model for ForeignKey

# class Organizations(db.Model):
#     __tablename__ = 'cisco_org_master'
#     __table_args__ = {"schema": "cam_db"}

#     org_id = db.Column(db.Integer, primary_key=True)
#     org_name = db.Column(db.String(45))
#     org_admin = db.Column(db.String(45))
#     status = db.Column(db.String(45))
#     created_by = db.Column(db.String(100))
#     created_date = db.Column(db.DateTime, default=datetime.datetime.now)
#     csp_id = db.Column(db.Integer, db.ForeignKey(Providers.csp_id), nullable=False)
#     org_entity_id = db.Column(db.String(45))
#     updated_by = db.Column(db.String(45))
#     update_date = db.Column(db.DateTime, default=datetime.datetime.now)
#     organization = db.relationship('Accounts', backref='fk_organization', lazy=True)
