# from mongoengine import Document, StringField, IntField, DateTimeField
import mongoengine as db
from datetime import datetime
import config
db.connect(config.DATABASE_NAME, host=config.DATABASE_URI)

class User(db.Document):
    email = db.StringField(required=True, max_length=100)
    first_name = db.StringField(required=True, max_length=50)
    last_name = db.StringField(required=True, max_length=50)
    password = db.StringField(default="")
    age = db.IntField(default=0)
    created_at = db.DateTimeField(default=datetime.utcnow)  # Default creation timestamp
    updated_at = db.DateTimeField(default=datetime.utcnow, on_modification=True) # update timestamp on update

    meta = {
        'collection': 'users'
    }
