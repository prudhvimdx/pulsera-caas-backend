import mongoengine as db
from models import models

class User(models.BaseDocument):
    email = db.StringField(required=True, max_length=100)
    first_name = db.StringField(required=True, max_length=50)
    last_name = db.StringField(required=True, max_length=50)
    password = db.StringField(default="")
    unsuccessful_login_attempts = db.IntField(default=0)
    age = db.IntField(default=0)

    meta = {
        'collection': 'users'
    }


class LoginHistory(models.BaseDocument):
    user_id = db.ReferenceField(User)
    device_type = db.StringField(max_length=10, default="web")
    logout_at = db.DateTimeField()

    meta = {
        'collection': 'login_history'
    }