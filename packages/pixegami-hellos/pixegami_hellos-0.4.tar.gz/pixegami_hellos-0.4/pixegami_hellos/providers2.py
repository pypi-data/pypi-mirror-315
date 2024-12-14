# import datetime
# from cam_db_config import db

# class Providers(db.Model):
#     __tablename__ = 'csp_vendor'
#     __table_args__ = {"schema": "cam_db"}

#     csp_id = db.Column(db.Integer, primary_key=True)
#     csp_name = db.Column(db.String(3), unique=True)
#     create_date = db.Column(db.DateTime, default=datetime.datetime.now)
#     csp_acct_mgr_name = db.Column(db.String(100))
#     csp_acct_mgr_email = db.Column(db.String(100))
#     csp_alt_email_1 = db.Column(db.String(100))
#     csp_alt_email_2 = db.Column(db.String(100))
