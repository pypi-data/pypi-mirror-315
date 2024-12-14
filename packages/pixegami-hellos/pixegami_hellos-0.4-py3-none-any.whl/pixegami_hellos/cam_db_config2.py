# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# from get_secrets import CREDS

# # import logging.config
# # import json
# # from sqlalchemy import create_engine

# # engine = create_engine('mysql+pymysql://root:Edytakorona1!@localhost/cam_db')

# app = Flask(__name__)

# # local config
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Pwd_1234@localhost/cam_db'

# app.config['DB_USER'] = CREDS['DB_USER']
# app.config['DB_PASSWD'] = CREDS['DB_PASSWD']
# app.config['DB_HOST'] = CREDS['DB_HOST']

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+app.config['DB_USER']+':'+app.config['DB_PASSWD']+\
#                                         '@'+app.config['DB_HOST']+'/cam_db'


# db = SQLAlchemy(app)
# PROV_ID_TO_CSP = ['', 'AWS', 'GCP', 'AZR']
# # with open('logging.json', 'r') as f:
# #     configInfo = json.load(f)
# #     logging.config.dictConfig(configInfo)