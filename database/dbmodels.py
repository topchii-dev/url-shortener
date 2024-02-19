import uuid
from database.db import db
import datetime

class Url(db.Model):
    __tablename__ = "urls"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    original_url = db.Column(db.Text, unique=True, nullable=False)
    shorten_url = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())

    def __repr__(self):
        return f"{self.id}, {self.original_url}, {self.shorten_url}, {self.created_at}"

    @property
    def serialize(self):
        return {
            'id': self.id,
            'original_url': self.original_url,
            'shorten_url': self.shorten_url,
            'created_at': self.created_at
        }
    
    @classmethod
    def create(cls, original_url, shorten_url):
        new_model = cls(original_url=original_url, shorten_url=shorten_url, created_at=datetime.datetime.now())
        db.session.add(new_model)
        db.session.commit()
        return new_model
    
    @classmethod
    def view_all(cls):
        return Url.query.all()
    
    @classmethod
    def view(cls, property_name, value):
        entry = Url.query.filter(getattr(Url, property_name) == value).first()
        return entry

    
    
