from flask_sqlalchemy import SQLAlchemy
from os import environ
base_de_datos=SQLAlchemy()

def areaConfigDB(app):
    app.config['SQLALCHEMY_DATABASE_URI']=environ.get('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    return app
