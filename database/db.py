from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

class DatabaseConnection:

    def __init__(self, db_name: str, uri: str):
        self.db_name = db_name
        self.database_uri = uri

    def init_app(self, application_instance: Flask):
        application_instance.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri + self.db_name
        application_instance.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(application_instance)
    
    def create_database(self, application_instance: Flask):
        from database.dbmodels import Url
    
        with application_instance.app_context():
            db.create_all()
            db.session.commit()
    
