import mongoengine as db
from models import models

class Terms(models.BaseDocument):
    type = db.StringField(required=True, max_length=20)
    content = db.StringField(default="")

    meta = {
        'collection': 'terms'
    }
